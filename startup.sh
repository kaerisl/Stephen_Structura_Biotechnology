git clone https://github.com/cryoem-uoft/structura-techchallenge-assets temp
mkdir db
mkdir dump
mkdir assets
mv temp/* assets/
rm -rf temp

mongod --dbpath db

for i in assets/*.jpg; do
    filename=$(echo $i | cut -f2 -d"/" | tr '\n' ' ')
    width=$(file $i | grep -Po ', [0-9]+x[0-9]+,' | cut -f1 -d"x" | cut -f2 -d" " | tr '\n' ' ')
    height=$(file $i | grep -Po ', [0-9]+x[0-9]+' | cut -f2 -d"x" | tr '\n' ' ')
    size=$(du -b $i | cut -f1 | tr '\n' ' ')
    python addFile.py $filename $width $height $size
done

# export FLASK_APP=main.py 
# flask run --port=3000