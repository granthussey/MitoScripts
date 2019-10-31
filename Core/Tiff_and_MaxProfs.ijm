
// FIRST: Make Tiff files

// Get the root folder containing .nd2 files
_RootFolder = getDirectory("Choose a Directory");

// Get the list of images to process from chosen directory.
_List = getFileList(_RootFolder);

// Initialize iterative variables.
item = 0;
nIm = 0;

// Create separate images.
setBatchMode(true);

// Initialize folder for Tiff files.
File.makeDirectory(_RootFolder + "TiffFiles");

// Run a for loop over the file list
while (item < _List.length)  {
	if ( endsWith(_List[item],".nd2") ) {

			run("Bio-Formats Importer", "open=" + _RootFolder + _List[item] + " color_mode=Default view=Hyperstack stack_order=XYCZT");
		  _Filename = replace(_RootFolder + "TiffFiles/" + _List[item],".nd2",".tif");
			saveAs("Tiff", _Filename);
			close();
		nIm++;
	}
	item++;
}

// If after loop no nIm++ called, then there were no .nd2 files.
// Otherwise, print number of processed .nd2 files.
if (nIm== 0) {
	showMessage("No nd2 files were found.");
} else {
	print("Number of nd2 files: " + nIm);
}

print("Tiff making is complete for " + _RootFolder);




// SECOND: Make Max Projection Stack

// Get dir of Tiff images
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

	if (ntiff == nIm) {
		print("Equal number of .nd2 tiles found to .tiff files created. All clear.");
	}

	print("A max projection was made in the first listed channel. Please ensure that is the MitoTracker channel.")
