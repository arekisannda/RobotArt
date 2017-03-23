mkdir ./res_png
for i in $(find ./test_path/ -type f);
do 
	new_name=./res_png/`basename $i .svg`".png"
	string="inkscape -z -e "$new_name" -w 400 -h 400 "$i	
	eval $string
done
