


_RootFolder = getDirectory("Choose a Directory");

// Defining the size in pixels of the single cell z-stacks
//_xy = getNumber("Single cell image size in pixels", 512);
_xy = 512'

// Creating a directory where the files are saved
_SaveDir = _RootFolder + "CellRox_Batch";
File.makeDirectory(_SaveDir);


setBatchMode(true);

run("ROI Manager...");
roiManager("Reset");
roiManager("Open",_RootFolder + "RoiSet.zip");

open("MaxProjs.tif");
MAXP = getImageID;

// For each ROI (cell)
for (roi = 0; roi < roiManager("count"); roi++) {

	roiManager("Select",roi);
	_FileName = getInfo("slice.label");
	_FileName = replace(_FileName,".tif","@");
	_FileName = split(_FileName,"@");
	_FileName = _FileName[0];

	open(_FileName + ".tif");
	TIFF = getImageID;
	run("Duplicate...", "duplicate channels=2");
	ORIGINAL = getImageID;
	close(TIFF);

	run("Restore Selection");

	newImage("CELL","16-bit Black",_xy,_xy,nSlices);
	CELL = getImageID;

	// Estimating the noise distribution around the ROI
	max_ai = 0;
	for (s = 1; s <= nSlices; s++) {
		selectImage(MAXP);

		selectImage(ORIGINAL);
		setSlice(s);
		run("Restore Selection");
		run("Make Band...", "band=5");
		getStatistics(area, mean, min, max, std);
		run("Restore Selection");
		run("Copy");

		selectImage(CELL);
		setSlice(s);
		run("Select None");
		run("Add...", "value=" + mean + " slice");
		run("Paste");

		getStatistics(area, mean, min, max, std);
		if (mean>max_ai) {
			max_ai = mean;
			slice_max_ai = s;
		}

	}

	run("Select None");
	resetMinAndMax();

	save(_SaveDir + "/" + _FileName + "_" + IJ.pad(roi,3) + ".tif");

	selectImage(CELL); close();
	selectImage(ORIGINAL); close();

}

selectImage(MAXP); close();

setBatchMode(false);

print("Cell croppping CellRoxBatch is complete.");
close("*");
