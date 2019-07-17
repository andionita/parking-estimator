
-- re-compute similarity vectors
DELETE FROM cluster_cosine_vectors;

WITH aux1 AS
  (SELECT aux2.cwithid AS cwithid,
          a.category AS dimid,
          SUM(array_length(string_to_array(array_to_string(aux2.amenity_list,'^'), a.name), 1) - 1) AS dimvalue
   FROM amenities a,
     (SELECT b.cwithid AS cwithid,
             array_agg(mbp.amenity) AS amenity_list
      FROM blocks b
      INNER JOIN merge_block_poi mbp ON b.block_id = mbp.block_id
      WHERE b.has_occupancy
      GROUP BY b.cwithid
      ORDER BY b.cwithid) AS aux2
   GROUP BY aux2.cwithid, a.category
   ORDER BY aux2.cwithid, a.category)
INSERT INTO cluster_cosine_vectors (cid, has_occupancy, dimid, dimvalue)
SELECT aux1.cwithid,
	   TRUE,
       aux1.dimid,
       aux1.dimvalue
FROM aux1;

WITH aux AS
  (SELECT temp.cwoutid AS cwoutid,
          a.category AS dimid,
          SUM((array_length(string_to_array(array_to_string(temp.amenity_list,'^'), a.name), 1) - 1)) AS dimvalue
   FROM amenities a,
     (SELECT b.cwoutid AS cwoutid,
             array_agg(mbp.amenity) AS amenity_list
      FROM blocks b
      INNER JOIN merge_block_poi mbp ON b.block_id = mbp.block_id
      WHERE NOT b.has_occupancy
      GROUP BY b.cwoutid
      ORDER BY b.cwoutid) AS TEMP
   GROUP BY TEMP.cwoutid, a.category
   ORDER BY TEMP.cwoutid, a.category)
INSERT INTO cluster_cosine_vectors (cid, has_occupancy, dimid, dimvalue)
SELECT aux.cwoutid,
	   FALSE,
       aux.dimid,
       aux.dimvalue
FROM aux;

/*
DELETE FROM cluster_vectors_wout;

WITH aux AS
  (SELECT temp.cwoutid AS cwoutid,
          a.type AS dimid,
          SUM((array_length(string_to_array(array_to_string(temp.amenity_list,'^'), a.name), 1) - 1)) AS dimvalue
   FROM amenities a,

     (SELECT b.cwoutid AS cwoutid,
             array_agg(mbp.amenity) AS amenity_list
      FROM blocks b
      INNER JOIN merge_block_poi mbp ON b.block_id = mbp.block_id
      WHERE NOT b.has_occupancy
      GROUP BY b.cwoutid
      ORDER BY b.cwoutid) AS TEMP
   WHERE a.name = ANY(TEMP.amenity_list)
   GROUP BY TEMP.cwoutid,
                 a.type)
INSERT INTO cluster_cosine_vectors (cid, has_occupancy, dimid, dimvalue)
SELECT aux.cwoutid,
	   FALSE,
       aux.dimid,
       aux.dimvalue
FROM aux;
*/

-- compute similarity values
DELETE FROM cluster_similarity;

WITH aux AS
  (SELECT cv1.cid AS cid1,
 		  cv1.has_occupancy AS has1,
          cv2.cid AS cid2,
          cv2.has_occupancy AS has2,
          SUM(cv1.dimvalue * cv2.dimvalue) / (SQRT(SUM(cv1.dimvalue * cv1.dimvalue))*SQRT(SUM(cv2.dimvalue * cv2.dimvalue))) AS cosine
   FROM cluster_cosine_vectors cv1
   INNER JOIN cluster_cosine_vectors cv2 ON cv1.dimid = cv2.dimid
   GROUP BY cv1.cid, cv1.has_occupancy,
            cv2.cid, cv2.has_occupancy)
INSERT INTO cluster_similarity (cid1, has1, cid2, has2, similarity, simtype)
SELECT aux.cid1,
       aux.has1,
       aux.cid2,
       aux.has2,
       aux.cosine,
       'cosine'
FROM aux;

-- remove the similarity between identical vectorss
DELETE FROM cluster_similarity WHERE cid1 = cid2 and has1 = has2;
