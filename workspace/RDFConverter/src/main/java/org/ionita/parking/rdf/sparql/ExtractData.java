package org.ionita.parking.rdf.sparql;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.ResultSet;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;

/**
 * Query the raw data inside the RDF-annotated SFpark data.
 * 
 * The SPARQL engine provided by Apache Jena is used.
 * 
 * @author Andrei Ionita
 *
 */
public class ExtractData {
	
	private static final String OCCUPANCY_RDF = "/sfpark_occupancy.ttl";
	private static final String OCCUPANCY_SPARQL = "/sfpark_occupancy.sparql";
	private static final String OCCUPANCY_CSV = "sfpark_occupancy_back.csv";
	
	private static final String TRAFFIC_RDF = "/sfpark_traffic.ttl";
	private static final String TRAFFIC_SPARQL = "/sfpark_traffic.sparql";
	private static final String TRAFFIC_CSV = "sfpark_traffic_back.csv";
	
	private static final String WEATHER_RDF = "/sfpark_weather.ttl";
	private static final String WEATHER_SPARQL = "/sfpark_weather.sparql";
	private static final String WEATHER_CSV = "sfpark_weather_back.csv";
	
	private static final String AMENITIES_RDF = "/poi_reduced.ttl";
	private static final String AMENITTIES_SPARQL = "/poi_reduced.sparql";
	private static final String AMENITIES_CSV = "poi_reduced_back.csv";
	
	private static final String LINE_SEPARATOR = System.getProperty("line.separator");

	public static void main(String[] args) throws IOException {
		
		String type = args[0];
		String rdfFile = null, sparqlFile = null, csvFile = null;
		switch (type) {
			case "occupancy":
				System.out.println("Extracting occupancy data...");
				rdfFile = OCCUPANCY_RDF;
				sparqlFile = OCCUPANCY_SPARQL;
				csvFile = OCCUPANCY_CSV;
				break;
			case "traffic":
				System.out.println("Extracting traffic data...");
				rdfFile = TRAFFIC_RDF;
				sparqlFile = TRAFFIC_SPARQL;
				csvFile = TRAFFIC_CSV;
				break;
			case "weather":
				System.out.println("Extracting weather data...");
				rdfFile = WEATHER_RDF;
				sparqlFile = WEATHER_SPARQL;
				csvFile = WEATHER_CSV;
				break;
			case "amenities":
				System.out.println("Extracting amenities data...");
				rdfFile = AMENITIES_RDF;
				sparqlFile = AMENITTIES_SPARQL;
				csvFile = AMENITIES_CSV;
				break;
		}
		
		System.out.println("RDF Input file: " + rdfFile);
		System.out.println("SPARQL file: " + sparqlFile);
		System.out.println("CSV Output file: " + csvFile);
		
		InputStream is = new FileInputStream(new File( ExtractData.class.getResource( rdfFile ).getFile()));
		
		Model model = ModelFactory.createDefaultModel();
		model.read( ExtractData.class.getResourceAsStream( rdfFile ), null, "ttl" );
		is.close();
		
		StringBuffer buffer = extractSPARQLQueryContent(sparqlFile);
		
		Query query = QueryFactory.create(buffer.toString());
		
		QueryExecution queryExecution = QueryExecutionFactory.create(query, model);
		ResultSet results = queryExecution.execSelect();
		
		//ResultSetFormatter.out(System.out, results, query);
		OutputStream os = new FileOutputStream( new File( csvFile )); 
		ResultSetFormatter.outputAsCSV(os, results);
		
		queryExecution.close();
	}

	private static StringBuffer extractSPARQLQueryContent( String sparqlFile) throws FileNotFoundException, IOException {
		BufferedReader reader = new BufferedReader(new FileReader( ExtractData.class.getResource( sparqlFile ).getFile() ));
		StringBuffer buffer = new StringBuffer();
		String line = null;
		while ( (line = reader.readLine()) != null ) {
			buffer.append(line + LINE_SEPARATOR);
		}
		reader.close();
		return buffer;
	}

}
