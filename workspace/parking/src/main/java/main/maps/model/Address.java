package main.maps.model;

import java.util.Locale;

public class Address {
	
	private String street;
	
	private String housenumber;
	
	private String city;
	
	private String district;
	
	private Locale locale;
	
	public void setStreet(String street) {
		this.street = street;
	}
	
	public String getStreet() {
		return street;
	}
	
	public void setHousenumber(String housenumber) {
		this.housenumber = housenumber;
	}
	
	public String getHousenumber() {
		return housenumber;
	}
	
	public void setCity(String city) {
		this.city = city;
	}
	
	public String getCity() {
		return city;
	}
	
	public void setDistrict(String district) {
		this.district = district;
	}
	
	public String getDistrict() {
		return district;
	}
	
	public void setLocale(Locale locale) {
		this.locale = locale;
	}
	
	public Locale getLocale() {
		return locale;
	}
	
	@Override
	public String toString() {
		if (locale != null && locale.equals( Locale.US )) 
			return housenumber + " " + street + ", " + city; //+ ", " + district;
		// for everywhere else
		return street + " " + housenumber + ", " + city; //+ ", " + district;
	}

}
