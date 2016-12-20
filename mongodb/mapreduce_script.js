var map = function() {
    var key = this.parkingarea;
    // parkingplace does not matter
    var value = this.isFree ? 1 : -1; 
    emit(key, value);
};

var reduce = function(key, values) {
    var delta = 0;
    values.forEach(
        function(value) {
            delta += value;
        }
    );
    return delta;   
};

db.sensordata.mapReduce( map, reduce, {
    out: { reduce: "currentstatus" },
    query: {
        timestamp: { $gt: new Date("2016-10-11T12:00T:00Z") }
    }
});

