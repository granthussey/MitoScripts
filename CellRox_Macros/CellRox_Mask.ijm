

_ImagingDir = getDirectory("Choose imaging dir");
_PNGDir = _ImagingDir + "PNG/"
_CellDir = _ImagingDir + "Cell/"

File.makeDirectory(_ImagingDir + "CellRox_Masks/");
File.makeDirectory(_ImagingDir + "CellRox_Results/");

		_Prefixes = get_image_prefixes(_PNGDir);

			for (i=0; i<_Prefixes.length; i++) {

				open(_PNGDir + _Prefixes[i] + ".png");
				MASK = getImageID;

				open(_CellDir + _Prefixes[i] + ".tif");
				CELL = getImageID;
				selectImage(CELL);

				run("Z Project...", "projection=[Sum Slices]");
				MAXP = getImageID;
				close(CELL);

				selectImage(MAXP);
				
				curFilename = "SUM_" + _Prefixes[i] + ".tif";
				arguement = "area mean min integrated median display redirect=" + curFilename + " decimal=3";
				run("Set Measurements...", arguement);
				run("Measure");

				close("*");

			}

			saveAs("Results",_ImagingDir + "CellRox_Results/" + "DivideTest.csv");

        function get_image_prefixes(theDir) {

			_List = getFileList(theDir);

			_Prefixes = newArray(_List.length)
			for (i=0; i<_List.length; i++) {

				_WithPng = replace(_List[i],".png","@");
				_WithPng = split(_WithPng,"@");
				_CurPrefix = _WithPng[0];
				_Prefixes[i] = _CurPrefix;
			}

			return _Prefixes;
        }
