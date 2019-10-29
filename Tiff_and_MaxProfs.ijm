


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

		_Filename = replace(_RootFolder + "TiffFiles/" + _List[item],".nd2",".tif");
		saveAs("Tiff", _Filename);
		close();

		im++;
	}
	item++;
}


print("Tiff making is complete.");


	TiffDir = _RootFolder + "TiffFiles/";

	item = 0;
	ntiff = 0;
	_List = getFileList(TiffDir);
	while (item < _List.length)  {
		if ( endsWith(_List[item],".tif") ) {
			if (ntiff==0) {
				open(TiffDir + _List[item]);
				w = getWidth();
				h = getHeight();
				close();
			}
			ntiff++;
		}
		item++;
	}
	if (ntiff== 0) {
		showMessage("No TIFF files were found.");
	} else {
		print("Number of TIFF files: " + ntiff);
	}

	// Generating the max projection stack

	newImage("MaxProjs", "16-bit black", w, h, ntiff);

	item = 0; im = 0;
	while (item < _List.length)  {
		if ( endsWith(_List[item],".tif") ) {
			im++;
			open(TiffDir + _List[item]);
			_FileName = split(_List[item],".");
			_FileName = _FileName[0];

			run("Z Project...", "start=1 stop=500 projection=[Max Intensity]");
			run("Copy");
			close();
			close();

			selectWindow("MaxProjs");
			setSlice(im);
			run("Paste");
			setMetadata("Label",_FileName);
		}
		item++;
	}

	// Saving max projection stack

	run("Save", "save=" +  TiffDir + "MaxProjs.tif");

	print("MaxProj making is complete. Proceed to cell cropping.");
