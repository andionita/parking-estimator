# Formats the JSON, copies it to the destination folder, saves it as Javascript and adds a variable assignment

python -m json.tool $1/$3.json > $2/$3.js

echo 'var json_'$3' = ' | cat - $2/$3.js > temp && mv temp $2/$3.js && rm $1/$3.json
