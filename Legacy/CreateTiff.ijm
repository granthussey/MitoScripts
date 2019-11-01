//run("Duplicate...", "duplicate frames=1");
//saveAs("Tiff", "/Users/granthussey/Desktop/MitoGraphTools/Exp2/Mito_dynamics_imaging_p53_4W_compressed.nd2");

_RootFolder = getDirectory("Choose a Directory");

//Get the list of images to process from chosen directory.
_List = getFileList(_RootFolder);



// Get the dimensions of the first image.
item = 0;
nIm = 0;

while (item < _List.length)  {
	if ( endsWith(_List[item],".nd2") ) {
		if (nIm==0) {
			//open(_RootFolder + _List[item]);
			run("Bio-Formats Importer", "open=" + _RootFolder + _List[item] + " color_mode=Default view=Hyperstack stack_order=XYCZT");
			print(_RootFolder + _List[item]);
			w = getWidth();
			h = getHeight();
			close();
		}
		nIm++;
	}
	item++;
}

// Quality Checking
if (nIm== 0) {
	showMessage("No nd2 files were found.");
} else {
	print("Number of nd2 files: " + nIm);
}


//Create separate images.
setBatchMode(true);

File.makeDirectory(_RootFolder + "TiffFiles");

item = 0; im = 0;
while (item < _List.length)  {
	if ( endsWith(_List[item],".nd2") ) {

		//open(_RootFolder + _List[item]);
		run("Bio-Formats Importer", "open=" + _RootFolder + _List[item] + " color_mode=Default view=Hyperstack stack_order=XYCZT");

		print(_RootFolder);
		print(_List[item]);

		_Filename = replace(_RootFolder + "TiffFiles/" + _List[item],".nd2",".tif");
		print(_Filename);

		saveAs("Tiff", _Filename);
		close();

		im++;
	}
	item++;
}


print("Tiff making is complete.");
