package org.ionita.parking.rdf.csv2rdf;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.Property;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.jena.riot.RDFFormat;
import org.apache.jena.vocabulary.RDF;
import org.ionita.parking.utils.RandomGenerator;

/**
 * Annotates CSV raw information from OpenStreetMap Points-of-interest
 * 
 * The CSV data has been preprocessed as to contain only the information relevant for this project.
 * 
 * The main ontology used is LinkedGeoData http://linkedgeodata.org
 * 
 * The RDF model is build using Apache Jena.
 * 
 * @author Andrei Ionita
 *
 */
public class AmenityConverter {

	// adjust in case the available memory is not enough to hold the Jena RDF model  
	private static int LINES_LIMIT = 5;

	private static final int ID_SIZE = 10;
	
	public static String CITYPULSE_OSM = "http://iot.ee.surrey.ac.uk/citypulse/datasets/osm/sfpark#";
	
	public static String CSV_FILE = "/poi_reduced.csv";
	public static String PREFIX_FILE = "/osm_prefixes.ttl";
	public static String TTL_OUTPUT_FILE = "poi_reduced.ttl";
	
	public static String CSV_SEPARATOR = ",";
	
	private static Property LGDO_NAME;
	private static Property LGDO_ID;
	private static Property GEOM;
	private static Property OGC_ASWKT;

	public static void main(String[] args) throws ParseException, FileNotFoundException {
		String[][] csvTable = readCSVFile(CSV_FILE);
		
		String prefixFileName = AmenityConverter.class.getResource( PREFIX_FILE ).getFile();
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
				
		for (int i = 1; i < csvTable.length; i++) {
			Resource observationPoint = model.createResource( CITYPULSE_OSM + RandomGenerator.getAlphanumeric(ID_SIZE));
			
			// amenity 
			String amenity = csvTable[i][2];
			amenity = amenity.substring(0, 1).toUpperCase() + amenity.substring(1);
			model.add(model.createStatement(observationPoint, RDF.type, model.createResource(model.expandPrefix("lgdo:" + amenity ))));
			
			// id
			observationPoint.addProperty(LGDO_ID, csvTable[i][0].trim());
			
			// geometry as WKT
			Resource geometryResource = model.createResource();
			observationPoint.addProperty(GEOM, geometryResource);
			geometryResource.addProperty(OGC_ASWKT, csvTable[i][10].trim());
			
			// name
			if ( csvTable[i][1].trim().length() > 0 ) {
				observationPoint.addProperty(LGDO_NAME, csvTable[i][1].trim());
			}
		}
				
		return model;
	}
		
	private static void setProperties(Model model) {
		LGDO_NAME = model.createProperty( model.expandPrefix("lgdo:name"));
		LGDO_ID = model.createProperty( model.expandPrefix("lgdo:id"));
		GEOM = model.createProperty( model.expandPrefix("geom:geometry"));
		OGC_ASWKT = model.createProperty( model.expandPrefix("ogc:asWKT"));
	}

	/**
	 * Reads in the CSV file containing the raw data
	 * 
	 * @param pathToCSVFile
	 * @return
	 */
	public static String[][] readCSVFile(String pathToCSVFile) {
		String filename = AmenityConverter.class.getResource( pathToCSVFile ).getFile();
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
