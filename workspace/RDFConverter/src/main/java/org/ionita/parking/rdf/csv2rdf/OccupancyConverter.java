package org.ionita.parking.rdf.csv2rdf;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TimeZone;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import org.apache.jena.vocabulary.RDF;
import org.ionita.parking.utils.RandomGenerator;

/**
 * Annotates CSV raw information on SFpark parking occupancy as provided by http://sfpark.org/
 * 
 * The CSV data has been preprocessed as to contain only the information relevant for this project.
 * 
 * The main ontology used is CityPulse http://www.ict-citypulse.eu
 * 
 * The RDF model is build using Apache Jena.
 * 
 * @author Andrei Ionita
 *
 */
public class OccupancyConverter {
	
	// adjust in case the available memory is not enough to hold the RDF model  
	private static int LINE_LIMITATION = 5;
	
	private static final int ID_SIZE = 10;

	public static String CITYPULSE_PARKING = "http://iot.ee.surrey.ac.uk/citypulse/datasets/parking/sfpark";
	public static String CITYPULSE_PARKING_OCCUPIED = "http://iot.ee.surrey.ac.uk/citypulse/datasets/parking/sfpark#occupied_spots";
	public static String CITYPULSE_PARKING_SPOTS = "http://iot.ee.surrey.ac.uk/citypulse/datasets/parking/sfpark#total_spots";
	
	public static String CSV_FILE = "/tuned_occupancy_030917_final.csv";
	public static String PREFIX_FILE = "/prefixes.ttl";
	public static String TTL_OUTPUT_FILE = "sfpark_occupancy.ttl";
	
	public static String CSV_SEPARATOR = ",";
	
	private static Property PROV_PROP;
	private static Property UNIT_PROP;
	private static Property VALUE_PROP;
	private static Property FOI_PROP;
	private static Property TIME_PROP;
	private static Property TIMEAT_PROP;
	private static Property FOI_PROP1;
	private static Property DBPEDIA_NO_SPACES;

	public static void main(String[] args) throws ParseException, FileNotFoundException {
		String[][] csvTable = readCSVFile(CSV_FILE);
		
		String prefixFileName = OccupancyConverter.class.getResource( PREFIX_FILE ).getFile();
		Map<String, String> prefixMap = RDFDataMgr.loadModel(prefixFileName).getNsPrefixMap();

		Model model = convert(csvTable, prefixMap);
					
		RDFDataMgr.write(new FileOutputStream(new File(TTL_OUTPUT_FILE)), model, RDFFormat.TURTLE_PRETTY);
	}

	/**
	 * Builds the RDF model based on the CSV data and the ontology prefixes
	 * 
	 * @param csvTable
	 * @param prefixMap
	 * @return
	 * @throws ParseException
	 */
	public static Model convert(String[][] csvTable, Map<String, String> prefixMap) throws ParseException {
		Model model = ModelFactory.createDefaultModel();
		model.setNsPrefixes(prefixMap);
		
		createProperties(model);
		
		createRDFModel(csvTable, model);
		
		return model;
	}

	private static void createRDFModel(String[][] csvTable, Model model) throws ParseException {
		// top level RDF statement that collects all observations
		Resource streamResource = model.createResource( CITYPULSE_PARKING );
		model.add(model.createStatement(streamResource, RDF.type, model.createResource(model.expandPrefix("sao:StreamEvent"))));
		
		List<Resource> occupiedSpotsPoints = new ArrayList<Resource>();
		
		for (int i = 1; i < csvTable.length; i++) {
			String id = RandomGenerator.getAlphanumeric(ID_SIZE);
						
			Resource occupiedSpotsRes = model.createResource( CITYPULSE_PARKING_OCCUPIED + "_" + id);
			model.add(model.createStatement(streamResource, PROV_PROP, occupiedSpotsRes));
			occupiedSpotsPoints.add(occupiedSpotsRes);			
		}
		
		Set<Resource> fois = new HashSet<Resource>();
		Map<String, String> blockMap = new HashMap<String, String>();
		
		String[] headers = csvTable[0];
		for (int i = 1; i < csvTable.length; i++ ) {
			int totalSpots = Integer.parseInt(csvTable[i][9]);
						
			//  occupied-spots points
			Resource observationPoint = occupiedSpotsPoints.get( i - 1);
			observationPoint.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			observationPoint.addProperty(UNIT_PROP, model.createResource( model.expandPrefix("unit0:vehicle-count")));
			double occupancyRate = Double.parseDouble(csvTable[i][10]);
			long occupiedSpots = Math.round(totalSpots * occupancyRate / 100);
			observationPoint.addProperty(VALUE_PROP, String.valueOf(occupiedSpots));

			// location as featureOfInterest
			Resource foi = model.createResource(headers[0] + "#" + csvTable[i][0]);
			fois.add(foi);
			observationPoint.addProperty(FOI_PROP, foi);
			Resource timeResource = model.createResource();
			observationPoint.addProperty(TIME_PROP, timeResource);
			timeResource.addProperty(RDF.type, model.expandPrefix("tl:Instant"));
			SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy HH:mm");
			sdf.setTimeZone(TimeZone.getTimeZone("GMT"));
			Date date = sdf.parse(csvTable[i][7]);
			
			// Jena always writes times to GMT, even if provided with a Calendar with a set timezone
			// so in order to preserve the datetime values, the fact that the times are American Pacific Coast time will be ignored
			Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("GMT"));
			cal.setTime(date);
			timeResource.addProperty(TIMEAT_PROP, model.createTypedLiteral(cal));

			// number of parking spaces
			observationPoint.addProperty(DBPEDIA_NO_SPACES, String.valueOf(totalSpots));
			
			// store block id information
			if ( ! blockMap.containsKey(csvTable[i][0])) {
				blockMap.put( csvTable[i][0], csvTable[i][0] );
			}
		}

		for (Resource foi : fois) {
			foi.addProperty(RDF.type, model.createResource(model.expandPrefix("sao:FeatureOfInterest")));
			Resource innerResource = model.createResource();
			foi.addProperty(FOI_PROP1, innerResource);
			innerResource.addProperty(RDF.type, model.createResource(model.expandPrefix("ct:Node")));
			String foiURI = foi.getURI();
			String blockDescription = blockMap.get( foiURI.substring( foiURI.indexOf("#") + 1) );
			innerResource.addProperty(model.createProperty(model.expandPrefix("ct:hasNodeName")), blockDescription);
		}
	}

	private static void createProperties(Model model) {
		PROV_PROP = model.createProperty( model.expandPrefix("prov:used"));
		UNIT_PROP = model.createProperty( model.expandPrefix("sao:hasUnitOfMeasurement"));
		VALUE_PROP = model.createProperty( model.expandPrefix("sao:value"));
		FOI_PROP = model.createProperty(model.expandPrefix("ns1:featureOfInterest"));
		TIME_PROP = model.createProperty(model.expandPrefix("sao:time"));
		TIMEAT_PROP = model.createProperty(model.expandPrefix("tl:at"));
		FOI_PROP1 = model.createProperty(model.expandPrefix("ct:hasFirstNode"));
		DBPEDIA_NO_SPACES = model.createProperty(model.expandPrefix("dbpedia-owl:numberOfParkingSpaces"));
	}

	/**
	 * Reads in the CSV file containing the raw data
	 * 
	 * @param pathToCSVFile
	 * @return
	 */
	public static String[][] readCSVFile(String pathToCSVFile) {
		String filename = OccupancyConverter.class.getResource( pathToCSVFile ).getFile();
		List<String[]> lines = new ArrayList<String[]>();
		try {
			BufferedReader br = new BufferedReader( new FileReader( new File( filename)));
			String s;
			while ( (s = br.readLine()) != null ) {
				String[] fields = s.split( "\"" + CSV_SEPARATOR + "\"|\"" + CSV_SEPARATOR + "|" + CSV_SEPARATOR + "\"|" + CSV_SEPARATOR + "|^\"|\"$");
				lines.add(fields);

				if (lines.size() == LINE_LIMITATION) {
					break;
				}
			}
			br.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return lines.toArray( new String[lines.size()][]);
	}

}
