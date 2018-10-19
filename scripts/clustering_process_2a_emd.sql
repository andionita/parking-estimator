-- prepare for Earth Mover's Distance 

-- take every amenity x and each cluster y and search the number of occurences of x in y's amenity list

DELETE FROM cluster_emd_gaussians;

WITH aux1 AS
  (SELECT aux2.cwithid AS cwithid,
          a.name AS dimid_name,
          (array_length(string_to_array(array_to_string(aux2.amenity_list,'^'), a.name), 1) - 1) AS dimvalue
   FROM amenities a,
     (SELECT b.cwithid AS cwithid,
             array_agg(mbp.amenity) AS amenity_list
      FROM blocks b
      INNER JOIN merge_block_poi mbp ON b.block_id = mbp.block_id
      WHERE b.has_occupancy
      GROUP BY b.cwithid
      ORDER BY b.cwithid) AS aux2
   WHERE a.name = ANY(aux2.amenity_list)
   ORDER BY aux2.cwithid,
                 a.name)
INSERT INTO cluster_emd_gaussians (cid, has_occupancy, dimname, dimvalue)
SELECT aux1.cwithid,
	   TRUE,
       aux1.dimid_name,
       aux1.dimvalue
FROM aux1;

WITH aux AS
  (SELECT temp.cwoutid AS cwoutid,
          a.name AS dimid_name,
          (array_length(string_to_array(array_to_string(temp.amenity_list,'^'), a.name), 1) - 1) AS dimvalue
   FROM amenities a,

     (SELECT b.cwoutid AS cwoutid,
             array_agg(mbp.amenity) AS amenity_list
      FROM blocks b
      INNER JOIN merge_block_poi mbp ON b.block_id = mbp.block_id
      WHERE NOT b.has_occupancy
      GROUP BY b.cwoutid
      ORDER BY b.cwoutid) AS TEMP
   WHERE a.name = ANY(TEMP.amenity_list)
   ORDER BY TEMP.cwoutid,
                 a.name)
INSERT INTO cluster_emd_gaussians (cid, has_occupancy, dimname, dimvalue)
SELECT aux.cwoutid,
	   FALSE,
       aux.dimid_name,
       aux.dimvalue
FROM aux;


