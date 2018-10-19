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
import java.util.GregorianCalendar;
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
 * Annotates CSV raw information on SFpark weather as provided by http://sfpark.org/
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
public class WeatherConverter {

	// adjust in case the available memory is not enough to hold the Jena RDF model  
	private static int LINES_LIMIT = 5;

	private static final int ID_SIZE = 10;

	public static String CITYPULSE_WEATHER = "http://iot.ee.surrey.ac.uk/citypulse/datasets/weather/sfpark";
	public static String CITYPULSE_WEATHER_OBS = "http://iot.ee.surrey.ac.uk/citypulse/datasets/weather/sfpark#observation";
	public static String CITYPULSE_WEATHER_MAXTEMP = "http://iot.ee.surrey.ac.uk/citypulse/datasets/weather/sfpark#max_temp";
	public static String CITYPULSE_WEATHER_MINTEMP = "http://iot.ee.surrey.ac.uk/citypulse/datasets/weather/sfpark#min_temp";
	public static String CITYPULSE_WEATHER_PRECIP = "http://iot.ee.surrey.ac.uk/citypulse/datasets/weather/sfpark#precipitation";
	
	public static String CSV_FILE = "/Weather.csv";
	public static String PREFIX_FILE = "/prefixes.ttl";
	public static String TTL_OUTPUT_FILE = "sfpark_weather.ttl";
	
	public static String CSV_SEPARATOR = ";";
	
	private static Property PROV_PROP;
	private static Property UNIT_PROP;
	private static Property FOI_PROP;
	private static Property VALUE_PROP;
	private static Property TIME_PROP;
	private static Property TIMEAT_PROP;
	private static Property FOIINNER_PROP;
	private static Property CTHASNODENAME_PROP;

	public static void main(String[] args) throws ParseException, FileNotFoundException {
		String[][] csvTable = readCSVFile(CSV_FILE);
		
		String prefixFileName = WeatherConverter.class.getResource( PREFIX_FILE ).getFile();
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
		Resource streamResource = model.createResource( CITYPULSE_WEATHER );
		model.add(model.createStatement(streamResource, RDF.type, model.createResource(model.expandPrefix("sao:StreamEvent"))));
		
		List<Resource> observationPoints = new ArrayList<Resource>();
		List<Resource> maxTempPoints = new ArrayList<Resource>();
		List<Resource> minTempPoints = new ArrayList<Resource>();
		List<Resource> precipPoints = new ArrayList<Resource>();
		
		for (int i = 1; i < csvTable.length; i++) {
			Resource observationPoint = model.createResource( CITYPULSE_WEATHER_OBS + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			observationPoints.add(observationPoint);
			model.add(model.createStatement(streamResource, PROV_PROP, observationPoint));
			
			Resource maxTempRes = model.createResource( CITYPULSE_WEATHER_MAXTEMP + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			maxTempPoints.add(maxTempRes);
			model.add(model.createStatement(observationPoint, PROV_PROP, maxTempRes));
						
			Resource minTempRes = model.createResource( CITYPULSE_WEATHER_MINTEMP + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			minTempPoints.add(minTempRes);
			model.add(model.createStatement(observationPoint, PROV_PROP, minTempRes));			
			
			Resource precipRes = model.createResource( CITYPULSE_WEATHER_PRECIP + "_" + RandomGenerator.getAlphanumeric(ID_SIZE));
			precipPoints.add(precipRes);
			model.add(model.createStatement(observationPoint, PROV_PROP, precipRes));
		}
		
		Set<Resource> fois = new HashSet<Resource>();
		Map<String, String> foiMap = new HashMap<String, String>();
				
		String[] headers = csvTable[0];
		for (int i = 1; i < csvTable.length; i++ ) {
			// weather observation node
			Resource observationPoint = observationPoints.get(i - 1);
			observationPoint.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			
			// maximum temperature
			Resource observationPointMaxTemp = maxTempPoints.get(i - 1);
			observationPointMaxTemp.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			observationPointMaxTemp.addProperty(UNIT_PROP, model.createResource( model.expandPrefix("unit3:degree-Fahrenheit")));
			int tempMax = Integer.parseInt(csvTable[i][2]);
			observationPointMaxTemp.addProperty(VALUE_PROP, String.valueOf(tempMax));
			
			// minimum temperature
			Resource observationPointMinTemp = minTempPoints.get(i - 1);
			observationPointMinTemp.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			observationPointMinTemp.addProperty(UNIT_PROP, model.createResource( model.expandPrefix("unit3:degree-Fahrenheit")));
			int tempMin = Integer.parseInt(csvTable[i][3]);
			observationPointMinTemp.addProperty(VALUE_PROP, String.valueOf(tempMin));
			
			// precipitation
			Resource precipPoint = precipPoints.get(i - 1);
			precipPoint.addProperty(RDF.type, model.createResource( model.expandPrefix("sao:Point")));
			precipPoint.addProperty(UNIT_PROP, model.createResource( model.expandPrefix("unit4:Inch")));
			int precipInch = Integer.parseInt(csvTable[i][4]);
			precipPoint.addProperty(VALUE_PROP, String.valueOf(precipInch));
						
			// dateTime
			Resource timeResource = model.createResource(replaceBlankspace(headers[1].trim()) + "#" + i);
			observationPoint.addProperty(TIME_PROP, timeResource);
			timeResource.addProperty(RDF.type, model.expandPrefix("tl:DateTimeInterval"));
			addTimestamp(csvTable, model, csvTable[i][1], timeResource);
			
			// location as featureOfInterest
			// store location information in a map
			String foiLocalName = replaceBlankspace(csvTable[i][0].trim());
			Resource foi = model.createResource(replaceBlankspace(headers[0].trim()) + "#" + foiLocalName);
			fois.add(foi);
			if ( ! foiMap.containsKey(csvTable[i][0])) {
				foiMap.put( foiLocalName, csvTable[i][0].trim() );
			}
			observationPoint.addProperty(FOI_PROP, foi);
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

	private static void addTimestamp(String[][] csvTable, Model model, String timestamp, Resource timeResource)
			throws ParseException {
		SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");
		TimeZone utc = TimeZone.getTimeZone("UTC");
		sdf.setTimeZone(utc);
		Date date = sdf.parse(timestamp);
		Calendar cal = new GregorianCalendar(utc);
		cal.setTime(date);
		// TODO dismiss time and pass only date to rdf
		timeResource.addProperty(TIMEAT_PROP, model.createTypedLiteral(cal));
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

	/**
	 * Reads in the CSV file containing the raw data
	 * 
	 * @param pathToCSVFile
	 * @return
	 */
	public static String[][] readCSVFile(String pathToCSVFile) {
		String filename = WeatherConverter.class.getResource( pathToCSVFile ).getFile();
		List<String[]> lines = new ArrayList<String[]>();
		try {
			BufferedReader br = new BufferedReader( new FileReader( new File( filename)));
			String s;
			while ( (s = br.readLine()) != null ) {
				String[] fields = s.split( "\"" + CSV_SEPARATOR + "\"|\"" + CSV_SEPARATOR + "|" + CSV_SEPARATOR + "\"|" + CSV_SEPARATOR + "|^\"|\"$");
				lines.add(fields);
				
				if (lines.size() == LINES_LIMIT) {
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
