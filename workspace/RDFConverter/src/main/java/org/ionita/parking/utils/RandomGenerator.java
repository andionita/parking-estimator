package org.ionita.parking.utils;

import java.util.Random;

/**
 * Utility class for generating random alphanumeric strings.
 * 
 * @author Andrei Ionita
 *
 */
public class RandomGenerator {
	
	public static String ALPHANUM = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
	
	public static String getAlphanumeric(int size) {
		Random random = new Random();
		StringBuilder builder = new StringBuilder();
		
		for ( int i = 0; i < size; i++ ) {
			builder.append( ALPHANUM.charAt(random.nextInt(ALPHANUM.length())));
		}
		
		return builder.toString();
	}

}
