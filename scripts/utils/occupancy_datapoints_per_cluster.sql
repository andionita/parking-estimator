SELECT cwithid,
       sum(occupancy_points) AS occupancy_datapoints_per_cluster
FROM blocks
WHERE has_occupancy
GROUP BY cwithid
ORDER BY occupancy_datapoints_per_cluster;