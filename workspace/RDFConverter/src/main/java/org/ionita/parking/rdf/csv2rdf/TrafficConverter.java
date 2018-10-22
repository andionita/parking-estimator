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
 * Annotates CSV raw information on SFpark traffic as provided by http://sfpark.org/
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
public class TrafficConverter {

	// adjust in case the available memory is not enough to hold the Jena RDF model  
	private static int LINES_LIMIT = 5;

	private static final int ID_SIZE = 10;
	
	public static String CITYPULSE_TRAFFIC = "http://iot.ee.surrey.ac.uk/citypulse/datasets/traffic/sfpark";
	public static String CITYPULSE_TRAFFIC_OBS = "http://iot.ee.surrey.ac.uk/citypulse/datasets/traffic/sfpark#observation";
	public static String CITYPULSE_TRAFFIC_VEHICLE = "http://iot.ee.surrey.ac.uk/citypulse/datasets/traffic/sfpark#vehicleCount";
	public static String CITYPULSE_TRAFFIC_SPEED = "http://iot.ee.surrey.ac.uk/citypulse/datasets/traffic/sfpark#averageSpeed";
	
	public static String CSV_FILE = "/sfpark_traffic.csv";
	public static String PREFIX_FILE = "/prefixes.ttl";
	public static String TTL_OUTPUT_FILE = "sfpark_traffic.ttl";
	
	public static String CSV_SEPARATOR = ",";
	
	private static Property PROV_PROP;
	private static Property UNIT_PROP;
	private static Property VALUE_PROP;
	private static Property FOI_PROP;
	private static Property TIME_PROP;
	private static Property TIMEAT_PROP;
	private static Property FOIINNER_PROP;
	private static Property CTHASNODENAME_PROP;

	public static void main(String[] args) throws ParseException, FileNotFoundException {
		String[][] csvTable = readCSVFile(CSV_FILE);
				
		String prefixFileName = TrafficConverter.class.getResource( PREFIX_FILE ).getFile();
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

		setProperties(model);
		
		// top level RDF statement that collects all observations
		Resource streamResource = model.createResource( CITYPULSE_TRAFFIC );
		model.add(model.createStatement(streamResource, RDF.type, model.createResource(model.expandPrefix("sao:StreamEvent"))));
		
		List<Resource> observationPoints = new ArrayList<Resource>();
		for (int i = 1; i < csvTable.length; i++) {
			Resource observationPoint = model.createResource( CITYPULSE_TRAFFIC_OBS + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			model.add(model.createStatement(streamResource, PROV_PROP, observationPoint));
			observationPoints.add(observationPoint);			
		}
		
		Set<Resource> fois = new HashSet<Resource>();
		Map<String, String> foiMap = new HashMap<String, String>();
		
		String[] headers = csvTable[0];		
		for (int i = 1; i < csvTable.length; i++ ) {
			Resource observationPoint = observationPoints.get(i - 1);
			observationPoint.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));

			// vehicle count
			Resource vehicleCountPoint = model.createResource( CITYPULSE_TRAFFIC_VEHICLE + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			model.add(model.createStatement(observationPoint, PROV_PROP, vehicleCountPoint));			
			vehicleCountPoint.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			vehicleCountPoint.addProperty(UNIT_PROP, model.createResource( model.expandPrefix("unit0:vehicle-count")));
			double vehicleCount = Double.parseDouble(csvTable[i][4]);
			vehicleCountPoint.addProperty(VALUE_PROP, String.valueOf(vehicleCount));

			// average speed
			Resource averageSpeedPoint = model.createResource( CITYPULSE_TRAFFIC_SPEED + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			model.add(model.createStatement(observationPoint, PROV_PROP, averageSpeedPoint));
			averageSpeedPoint.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			averageSpeedPoint.addProperty(UNIT_PROP, model.createResource( model.expandPrefix("unit2:km-per-hour")));
			double averageSpeed = Double.parseDouble(csvTable[i][5]);
			averageSpeedPoint.addProperty(VALUE_PROP, String.valueOf(averageSpeed));
			
			// location as feaureOfInterest
			// store location information in a map
			String foiLocalName = replaceBlankspace(csvTable[i][0].trim());
			Resource foi = model.createResource(replaceBlankspace(headers[0].trim()) + "#" + foiLocalName);
			fois.add(foi);
			if ( ! foiMap.containsKey(csvTable[i][0])) {
				foiMap.put( foiLocalName, csvTable[i][0] );
			}
			observationPoint.addProperty(FOI_PROP, foi);
			
			// time
			Resource timeResource = model.createResource(replaceBlankspace(headers[3].trim()) + "#" + RandomGenerator.getAlphanumeric(ID_SIZE));
			observationPoint.addProperty(TIME_PROP, timeResource);
			timeResource.addProperty(RDF.type, model.expandPrefix("tl:Instant"));
			setDateTime(csvTable, model, TIMEAT_PROP, csvTable[i][3], timeResource);
		}

		for (Resource foi : fois) {
			foi.addProperty(RDF.type, model.createResource(model.expandPrefix("sao:FeatureOfInterest")));
			Resource innerResource = model.createResource();
			foi.addProperty(FOIINNER_PROP, innerResource);
			innerResource.addProperty(RDF.type, model.createResource(model.expandPrefix("ct:Node")));
			String foiURI = foi.getURI();
			String location = foiMap.get( foiURI.substring( foiURI.indexOf("#") + 1) );
			innerResource.addProperty(CTHASNODENAME_PROP, location);
		}
		
		return model;
	}
	
	private static String replaceBlankspace(String s) {
		return s.replace(" ", "_");
	}

	private static void setProperties(Model model) {
		PROV_PROP = model.createProperty( model.expandPrefix("prov:used"));
		UNIT_PROP = model.createProperty( model.expandPrefix("sao:hasUnitOfMeasurement"));
		VALUE_PROP = model.createProperty( model.expandPrefix("sao:value"));
		FOI_PROP = model.createProperty(model.expandPrefix("ns1:featureOfInterest"));
		TIME_PROP = model.createProperty(model.expandPrefix("sao:time"));
		TIMEAT_PROP = model.createProperty(model.expandPrefix("tl:at"));
		FOIINNER_PROP = model.createProperty(model.expandPrefix("ct:hasFirstNode"));
		CTHASNODENAME_PROP = model.createProperty(model.expandPrefix("ct:hasNodeName"));
	}

	private static void setDateTime(String[][] csvTable, Model model, Property timeAtProp, String timestamp, Resource timeResource)
			throws ParseException {
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		sdf.setTimeZone(TimeZone.getTimeZone("GMT"));
		Date date = sdf.parse(timestamp);
		
		// Jena always writes times to GMT, even if provided with a Calendar with a set timezone
		// so in order to preserve the datetime values, the fact that the times are American Pacific Coast time will be ignored
		Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("GMT"));
		cal.setTime(date);
		
		timeResource.addProperty(timeAtProp, model.createTypedLiteral(cal));
	}

	/**
	 * Reads in the CSV file containing the raw data
	 * 
	 * @param pathToCSVFile
	 * @return
	 */
	public static String[][] readCSVFile(String pathToCSVFile) {
		String filename = TrafficConverter.class.getResource( pathToCSVFile ).getFile();
		List<String[]> lines = new ArrayList<String[]>();
		try {
			BufferedReader br = new BufferedReader( new FileReader( new File( filename)));
			String s;
			while ( (s = br.readLine()) != null ) {
				String[] fields = s.split( "\"" + CSV_SEPARATOR + "\"|\"" + CSV_SEPARATOR + "|" + CSV_SEPARATOR + "\"|" + CSV_SEPARATOR + "|^\"|\"$");
				lines.add(fields);
				if (lines.size() == LINES_LIMIT)
					break;
			}
			br.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return lines.toArray( new String[lines.size()][]);
	}

}
