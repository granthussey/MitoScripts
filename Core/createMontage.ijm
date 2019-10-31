

assess_images();

                function assess_images() {

                _ImagingDir = getDirectory("Select the imaging directory");

                _No_Gauss_PNG_Dir = _ImagingDir + "GaussPNG/";
                _No_Gauss_Cell_Dir = _ImagingDir + "Gauss_BatchCells/";

                _Gauss_PNG_Dir = _ImagingDir + "NoGaussPNG/";
                _Gauss_Cell_Dir = _ImagingDir + "NoGauss_BatchCells/";

                File.makeDirectory(_ImagingDir + "Montages");

                _Prefixes = get_image_prefixes();

                nMontage = floor(_Prefixes.length/5) + 1;
                iMontage = 0;

                        n = 0;

                        for (i=0; i<_Prefixes.length; i++) {

                                open(_No_Gauss_Cell_Dir + _Prefixes[i] + ".tif");
                                run("Z Project...", "start=1 stop=500 projection=[Max Intensity]");
                                selectWindow(_Prefixes[i] + ".tif");
                                close();
                                selectWindow("MAX_" + _Prefixes[i] + ".tif");
                                run("8-bit");
                                run("Enhance Contrast", "saturated=0.35");

                                open(_No_Gauss_PNG_Dir + _Prefixes[i] + ".png");
                                run("Enhance Contrast", "saturated=0.35");

                                open(_Gauss_Cell_Dir + _Prefixes[i] + ".tif");
                                run("Z Project...", "start=1 stop=500 projection=[Max Intensity]");
                                selectWindow(_Prefixes[i] + ".tif");
                                close();
                                selectWindow("MAX_" + _Prefixes[i] + "-1.tif");
                                run("8-bit");
                                run("Enhance Contrast", "saturated=0.35");

                                open(_Gauss_PNG_Dir + _Prefixes[i] + ".png");
                                run("Enhance Contrast", "saturated=0.35");

                                n++ ;

                                if (n == 4) {

                                        n = 0;
                                        iMontage++;

                                        run("Images to Stack", "name=Stack title=[] use");
                                        run("Make Montage...", "columns=4 rows=4 scale=1 font=20 label");
                                        close("\\Others");

                                        save(_ImagingDir + "Montages/" + iMontage +  ".tif");

                                        }

                                else{}

                                if (i == _Prefixes.length-1) {n = 0;
                                        iMontage++;

                                        run("Images to Stack", "name=Stack title=[] use");
                                        run("Make Montage...", "columns=5 rows=4 scale=1 font=20 label");

                                        save(_ImagingDir + "Montages/" + iMontage +  ".tif");

                                        close("*");

                                        }

                                        else{}
                        }

                        print(nMontage);

                }

        function get_image_prefixes() {

                        _RootFolder = getDirectory("Choose a directory with prefixes");
                        _List = getFileList(_RootFolder);

                        _Prefixes = newArray(_List.length)
                        for (i=0; i<_List.length; i++) {

                                _WithPng = replace(_List[i],".png","@");
                                _WithPng = split(_WithPng,"@");
                                _CurPrefix = _WithPng[0];
                                _Prefixes[i] = _CurPrefix;
                        }

                        return _Prefixes;
        }
                                                                                                                                                                                                                            115,1         Bot
