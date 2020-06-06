cd dataset

for i in *.rtf ; do 
    textutil -convert txt "$i" ${i/.rtf}.txt
done

cd ..