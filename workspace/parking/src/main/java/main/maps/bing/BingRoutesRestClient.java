package main.maps.bing;

import java.io.IOException;
import java.net.URLEncoder;
import java.util.Locale;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.apache.http.client.fluent.Content;
import org.apache.http.client.fluent.Request;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import main.maps.model.Address;

public class BingRoutesRestClient {
	
	private static final String BING_API_KEY = "AgLHCZFelVbOW9uE6FJ043qT8MAf3x7XD_fYRQMyoNcF2_7XWvk6O2gwAYeBe_4o";
	
	private static final String WALKING_DISTANCE_URL = "http://dev.virtualearth.net/REST/V1/Routes/Walking?wp.0=%s&wp.1=%s&optmz=distance&output=xml&key=" + BING_API_KEY;

	public static void calculateDistance(Address address1, Address address2) {		
		try {
			String urlStr = String.format(WALKING_DISTANCE_URL, 
								URLEncoder.encode(address1.toString(), "UTF-8"), 
								URLEncoder.encode(address2.toString(), "UTF-8"));
			Content content = Request.Get( urlStr ).execute().returnContent();
			System.out.println(content);
			
			DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
			Document doc = builder.parse(content.asStream());
			
			XPath xpath = XPathFactory.newInstance().newXPath();
			XPathExpression durationExpr = xpath.compile("string(/Response/ResourceSets/ResourceSet/Resources/Route/TravelDuration)");
			XPathExpression durationUnitExpr = xpath.compile("string(/Response/ResourceSets/ResourceSet/Resources/Route/DurationUnit)");
			XPathExpression distanceExpr = xpath.compile("string(/Response/ResourceSets/ResourceSet/Resources/Route/TravelDistance)");
			XPathExpression distanceUnitExpr = xpath.compile("string(/Response/ResourceSets/ResourceSet/Resources/Route/DistanceUnit)");
			String duration = (String) durationExpr.evaluate(doc, XPathConstants.STRING);
			String durationUnit = (String) durationUnitExpr.evaluate(doc, XPathConstants.STRING);
			String distance = (String) distanceExpr.evaluate(doc, XPathConstants.STRING);
			String distanceUnit = (String) distanceUnitExpr.evaluate(doc, XPathConstants.STRING);
			
			System.out.println( duration + " " + durationUnit );
			System.out.println( distance + " " + distanceUnit );
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParserConfigurationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SAXException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (XPathExpressionException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
	
	public static void main(String[] args) {
		Address address1 = new Address();
		address1.setStreet("2nd Avenue");
		address1.setHousenumber("200");
		address1.setCity("San Francisco");
		//address1.setDistrict("CA");
		address1.setLocale(Locale.US);
		
		Address address2 = new Address();
		address2.setStreet("2nd Avenue");
		address2.setHousenumber("201");
		address2.setCity("San Francisco");
		//address2.setDistrict("CA");
		address2.setLocale(Locale.US);
		
		calculateDistance(address1, address2);
	}

}
