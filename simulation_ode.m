%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                              UNICORN - 2 SIMULATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Description....
%
% INPUTS:
%   
%   
% OUTPUTS:
%   
%   
% AUTHOR:
%   Adam Bell, Matteo Ceriotti @ Alba Orbital, 27/08/2018
%   Scott Hurley, 09/08/2019
%
% CHANGELOG:
%   29/08/18, Adam Bell: changed euler angles form individual elements to elements an array.
%   Extraction of orbital elements from TLE moved to function 'extract_tle'.
%
%   10/09/18 , Adam: added centre of mass and surface area to SATELLITE.
%
%   31/05/19, Adam: addition of some preliminary ground station / satellite tracking.
%
%   09/08/19, Scott: Added a GUI

close all; clc; clear;
clear dynAttitude;      % To clear persistent variables within the function
tic

%% ------------------------------------------------------------------------------
%% GLOBAL VARIABLES

close all;
clear h;
global tle1u = [1   40074    14037   19274.00  .00000291  00000-0  42223-4   0   9995]; 
global tle2u = [2   40074    97.01    134.87      .0001          0.0000001  0         15.6092];
global tfu  = 0.001 * 5500;
global errorFlags = [0 0 0 0 0 0 0];
global simRuns = 1;
global alt = 6756765.2955854739766551451390369;
global dirpath = '';
global widgets;
global f = figure('Name','Simulation GUI','NumberTitle','off');
global fh = get(groot,'CurrentFigure');
global userInput = {'00/00/00/01/10/19' '97.01' '134.87' '0.0000001' '0' '6756765.2955854739766551451390369' '1'};

%% ------------------------------------------------------------------------------

set(f, 'MenuBar', 'None');

%Standard gravitational parameter for Earth.
mu = 3.9860043543609598e+05;

%Updates the userInput cell with parameters loaded from file.
function updateVariables(h)
  global tfu;
  global userInput;
  editDate(char(userInput(1)), h);
  editIncl(char(userInput(2)), h);
  editRAAN(char(userInput(3)), h);
  editArgPer(char(userInput(4)), h);
  editMeanAnom(char(userInput(5)), h);
  editAltd(char(userInput(6)), h);
  editNoOfOrbits(char(userInput(7)), h);
endfunction

%Checks whether a selected text file has the correct format
function validFormat = loadParameters(fileName, h)
  global userInput;
  global fh;
  
  fileID = fopen(fileName,'r');
  formatSpec = '%s';
  tline = fgetl(fileID);
  vars = {};
  validFormat = true;
  i = 1;
  while ischar(tline) 
    vars{end+1} = tline;
    tline = fgetl(fileID);
    ++i;
  endwhile
  
  fclose(fileID);
  
  if (length(vars) != 7)
    validFormat = false;
  endif
  
  i = 1;
  if (!checkDate(vars{i}))
    validFormat = false;
  endif
  i = 2;
  while i <= length(vars)
    isNan = isnan(str2double(vars{i}));
    if (isNan && str2num(vars{i}) < 0)
      validFormat = false;
    endif
    ++i;
  endwhile
  if validFormat
    i = 1;
    while(i <= length(userInput))
      userInput(i) = vars{i};
      ++i;
    endwhile
    editText();
    updateVariables(h);
  endif
endfunction

%Clears global variables when the main window is closed.
function closeRequest(obj, init = false)
  global fh;
  clear all;
  fh = get(groot,'CurrentFigure');
  delete(fh);
endfunction



%Loads previously entered values into edit fields.
function editText()
  global widgets;
  global userInput;
  if(!strcmp("", userInput(1)))
    set(widgets(1),'string',userInput(1));
  endif
  if(!strcmp("", userInput(2)))
    set(widgets(2),'string',userInput(2));
  endif
  if(!strcmp("", userInput(3)))
    set(widgets(3),'string',userInput(3));
  endif
  if(!strcmp("", userInput(4)))
    set(widgets(4),'string',userInput(4));
  endif
  if(!strcmp("", userInput(5)))
    set(widgets(5),'string',userInput(5));
  endif
  if(!strcmp("", userInput(6)))
    set(widgets(6),'string',userInput(6));
  endif
  if(!strcmp("", userInput(7)))
    set(widgets(7),'string',userInput(7));
  endif
endfunction

%Edits the date value of TLE1 using the value from userInput.
function editDate(value, h)
  global userInput;
  global tle1u;
  global errorFlags;
  if(checkDate(value))
        userInput(1) = value;
        tle1u(4) = convertDate(value);
        errorFlags(1) = 0;
        displayError(h);
      else
        errorFlags(1) = 1; 
        displayError(h);     
      endif
endfunction

%Edits the inclination value of TLE2 using the value from userInput.
function editIncl(value, h)
  global userInput;
  global tle2u;
  global errorFlags;
  isNan = isnan(str2double(value));
  if(!isNan && str2num(value) >= 0)
        userInput(2) = value;
        tle2u(3) = str2num(value);
        errorFlags(2) = 0;
        displayError(h);
      else
        errorFlags(2) = 1;
        displayError(h);
      endif
endfunction

%Edits the RAAN value of TLE2 using the value from userInput.
function editRAAN(value, h)
  global userInput;
  global tle2u;
  global errorFlags;
  isNan = isnan(str2double(value));
  if(!isNan && str2num(value) >= 0)
        userInput(3) = value;
        tle2u(4) = str2num(value);
        errorFlags(3) = 0;
        displayError(h);
      else
        errorFlags(3) = 1;
        displayError(h);
      endif
endfunction

%Edits the argument of perigree value of TLE2 using the value from userInput.
function editArgPer(value, h)
  global userInput;
  global tle2u;
  global errorFlags;
  isNan = isnan(str2double(value));
  if(!isNan && str2num(value) >= 0)
        userInput(4) = value;
        tle2u(6) = str2num(value);
        errorFlags(4) = 0;
        displayError(h);
      else
        errorFlags(4) = 1;
        displayError(h);
      endif
endfunction

%Edits the mean anomoly value of TLE2 using the value from userInput.
function editMeanAnom(value, h)
  global userInput;
  global tle2u;
  global errorFlags;
  isNan = isnan(str2double(value));
  if(!isNan && str2num(value) >= 0)
        userInput(5) = value;
        tle2u(7) = str2num(value);
        errorFlags(5) = 0;
        displayError(h);
      else
        errorFlags(5) = 1;
        displayError(h);
      endif
endfunction

%Edits the revolutions/day value of TLE2 using the altitiude from userInput.
function editAltd(value, h)
  global alt;
  global userInput;
  global tle2u;
  global errorFlags;
  isNan = isnan(str2double(value));
  if(!isNan && str2num(value) >= 0)
        alt = str2num(value);
        userInput(6) = value;
        tle2u(8) = alttorevsday();
        errorFlags(6) = 0;
        displayError(h);
      else
        errorFlags(6) = 1;
        displayError(h);
      endif
endfunction

%Edits the tf using the value from simRuns.
function editNoOfOrbits(value, h)
  global userInput;
  global errorFlags;
  global simRuns;
  isNan = isnan(str2double(value));
  if(!isNan && str2num(value) > 0)
    userInput(7) = value;
    simRuns = str2num(value);
    errorFlags(7) = 0;
    displayError(h);
  else
    errorFlags(7) = 1;
    displayError(h);
  endif
endfunction

%Callback function for user interaction with the main window.
function callBack(obj, init = false)
  global tle1u;
  global tle2u;
  global simRuns;
  global tfu;
  global fh;
  global errorFlags;
  global alt;
  global dirpath;
  h = guidata (obj);
  value = get (gcbo, "string");
  switch (gcbo)
    case{h.dateTxt}
      editDate(value, h);
    case{h.inclnTxt}
      editIncl(value, h);
    case{h.raanTxt}
      editRAAN(value, h);
    case{h.argPerTxt}
      editArgPer(value, h);
    case{h.meanAnomTxt}
      editMeanAnom(value, h);
    case{h.altdTxt}
      editAltd(value, h);
    case{h.noOrbsTxt}
      editNoOfOrbits(value, h);
    case{h.runSimButton}
      if (simRuns > 0 && alt >= 0)     
        tfu = orbitsToSec();    
      endif
      if(!(sum(errorFlags) > 0))
        delete(findall(gcf,'type','uicontrol'));
        fh = get(groot,'CurrentFigure');
        makeFolder();
        saveParameters();
        run_sim(tle1u, tle2u, tfu, dirpath);
        createList();
      endif
    case{h.loadParamButton}   
      [fname, fpath, fltidx]  = uigetfile ("parameter.txt");
      if(fname != 0)
        validFormat = loadParameters([fpath fname], h);
        if(validFormat)
          dirpath = fpath;
          delete(findall(gcf,'type','uicontrol'));
          fh = get(groot,'CurrentFigure');
          createList();
        else
          f = errordlg('Incorrect file format','Load Error');
        endif
      endif
    case{h.loadFigButton}
      [fname, fpath, fltidx]  = uigetfile ("*.ofig");
      if(fname != 0)
        h = hgload ([fpath fname]);
      endif
  endswitch
endfunction

%Writes user input parameters to file.
function saveParameters()
  global userInput;
  global dirpath;
  fid = fopen([dirpath 'parameter.txt'], 'wt');
  i = 1;
  while(i <= 7)
    fprintf(fid, '%s\n', char(userInput(i)));
    ++i;
  endwhile
  fclose(fid);
endfunction

%Creates the main window for the GUI, where the user inputs parameters and loads files.
function createMainWindow()
  global f;
  global widgets;
  delete(findall(gcf,'type','uicontrol'));
  widgets = zeros(1, 7);
  p = uipanel ("title", "Input Fields", "position", [.0 .0 1 1]);
  
  h.errorTxt = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "",
       "horizontalalignment", "left",
       "position", [0.01 0.01 0.4 0.04]
    );
  
  h.dateLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "Date(SS/MM/HH/DD/MM/YY):",
       "horizontalalignment", "left",
       "position", [0.01 0.885 0.31 0.04]
    );

  %input format: SS/MM/HH/DD/MM/YY
  %time is 24hr
  h.dateTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "00/00/00/01/10/19",
       "callback", @callBack,
       "position", [190 367 240 20]
    );
  widgets(1) = h.dateTxt;
    
  h.inclnLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "Inclination:",
       "horizontalalignment", "left",
       "position", [0.01 0.82 0.20 0.04]
    );

  h.inclnTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "97.01",
       "callback", @callBack,
       "position", [190 340 240 20]
    );
  widgets(2) = h.inclnTxt;

  h.raanLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "RAAN:",
       "horizontalalignment", "left",
       "position", [0.01 0.755 0.20 0.04]
    );

  h.raanTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "134.87",
       "callback", @callBack,
       "position", [190 313 240 20]
    );
  widgets(3) = h.raanTxt;

  h.argPerLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "Argument of perigee:",
       "horizontalalignment", "left",
       "position", [0.01 0.69 0.22 0.04]
    );

  h.argPerTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "0.0000001",
       "callback", @callBack,
       "position", [190 286 240 20]
    );
  widgets(4) = h.argPerTxt;

  h.meanAnomLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "Mean Anomoly:",
       "horizontalalignment", "left",
       "position", [0.01 0.625 0.20 0.04]
    );

  h.meanAnomTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "0",
       "callback", @callBack,
       "position", [190 259 240 20]
    );
  widgets(5) = h.meanAnomTxt;

  h.altdLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "Altitude(metres from surface):",
       "horizontalalignment", "left",
       "position", [0.01 0.56 0.31 0.04]
    );

  h.altdTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "6756765.2955854739766551451390369",
       "callback", @callBack,
       "position", [190 232 240 20]
    );
  widgets(6) = h.altdTxt;

  h.noOrbsLabel = uicontrol (f,
       "style", "text",
       "units", "normalized",
       "string", "Number of Orbits:",
       "horizontalalignment", "left",
       "position", [0.01 0.495 0.20 0.04]
    );

  h.noOrbsTxt = uicontrol (f,
       "style", "edit",
       "units", "pixels",
       "string", "1",
       "callback", @callBack,
       "position", [190 205 240 20]
    );
  widgets(7) = h.noOrbsTxt;
    
  h.runSimButton = uicontrol(
      mainForm = "style", "pushbutton", "string", "Run Simulation", "callback", 
                  @callBack, "position", [190 170 150 20]
    );
    
  h.loadParamButton = uicontrol(
      mainForm = "style", "pushbutton", "string", "Load Parameters", "callback", 
                  @callBack, "position", [445 390 110 20]
    );            
  h.loadFigButton = uicontrol(
      mainForm = "style", "pushbutton", "string", "Load Figure", "callback", 
                  @callBack, "position", [445 365 110 20]
    );
    
  set (gcf, "color", get(0, "defaultuicontrolbackgroundcolor"))
  set(f,'CloseRequestFcn',@closeRequest)
  guidata (gcf, h)
endfunction

%Displays an appropiate error message for erroneous user input.
function displayError(h)
  global errorFlags;
  errors ={"Invalid date", "Invalid inclination", "Invalid RAAN", "Invalid arg of per", "Invalid mean anomoly", "Invalid altitude", "Invalid number of orbits"};
  i = 1;
  while(i <= length(errorFlags))
    if(errorFlags(i) == 1)
      set(h.errorTxt, 'String', errors{i});
      break;
    endif
    set(h.errorTxt, 'String', "");
    ++i;
  endwhile
endfunction

%Determines if a string represents a valid date (SS/MM/HH/DD/MM/YY).
function isValidDate = checkDate(date)
  validLength = (length(date) == 17);
  
  if(validLength)
    hours = str2num(substr(date, 7, 2));
    minutes = str2num(substr(date, 4, 2));
    seconds = str2num(substr(date, 1, 2));
    validTime = hours >= 0 && hours < 24 && minutes >= 0 && minutes < 60 && seconds >= 0 && seconds < 60;
  
    bools = isstrprop (date, 'digit');
    i = 1;
    validType = true;
    
    while(i < 18)
      if(mod(i, 3) == 0)
        1+1;
      elseif(!bools(i))
        validType = false;
        break;
      endif
    ++i;
    endwhile
    
    month = str2num(substr(date, -5, -3));
    validMonth = month < 13 && month > 0;
    
    year = str2num(substr(date, -2));
    day = str2num(substr(date, -8, -6));
    validDay = true;
    
    if((month == 1 || month == 3 || month == 5 || month == 7 
      || month == 8 || month == 10) && (day > 31 || day < 1))
      validDay = false;
    %Checks if its a leap year and February.
    elseif(month == 2)
        if((mod(year,4) == 0) && (day > 29 || day < 1))
          validDay = false;
        elseif((mod(year,4) != 0) && (day > 28 || day < 1))
          validDay = false;
        endif
    elseif((month == 4 || month == 6 || month == 9 || month == 11 
          || month == 12) && (day > 30 || day < 1))
        validDay = false;
    endif
    validFormat = true;
    if(date(3) != '/' || date(6) != '/' || date(9) != '/' || date(12) != '/' ||
      date(15) != '/')
      validFormat = false;
    endif
    isValidDate = validTime && validLength && validType && validMonth && validDay && validFormat;
  else
    isValidDate = validLength;
  endif
endfunction

%Converts the date in the format 'SS/MM/HH/DD/MM/YY' to 'YYDDD.DD'.
function newDate = convertDate(date) 
  year = substr(date, -2);
  month = substr(date, -5, -3);
  day = substr(date, -8, -6);
  hours = substr(date, 7, 2);
  minutes = substr(date, 4, 2);
  seconds = substr(date, 1, 2);
  newDate = (str2num(year) .* 1000) + convertMonth(str2num(month), str2num(year)) + str2num(day) + convertDecimalDay(str2num(seconds), str2num(minutes), str2num(hours));
endfunction

%Calculates the number of orbits a body completes in a day around Earth.
function revsday = alttorevsday()
  global alt;
  if(alt == 0)
    revsday = 0;
  else
    period = calcPeriod();
    revsday = 86400/period;
  endif
endfunction

%Calculates the orbital period of an object around Earth.
function period = calcPeriod()
  global alt;
  talt = alt + 6370;
  talt = talt ^ 3;
  temp = talt / 3.9860e14;
  temp = sqrt(temp);
  period = 2 * pi * temp;
endfunction

%Converts the number of orbits requested to the time (seconds) needed for the 
%simulation to run.
function secs = orbitsToSec()
  global alt;
  global simRuns;
  secs = simRuns * calcPeriod(alt);
endfunction

%Converts the seconds, minutes and hours passed in the day to decimal day.
function decimalDay = convertDecimalDay(seconds, minutes, hours)
  minutesecs = minutes * 60;
  hoursecs = hours * 60 * 60;
  decimalDay = ((seconds + minutesecs + hoursecs) / 86400);
endfunction

%Converts the number of months into the number of days passed.
function day = convertMonth(month, year)
  day = 0;
  month = month -1;
  while(month > 0)
    if(month == 1 || month == 3 || month == 5 || month == 7 
      || month == 8 || month == 10 || month == 12)
      day+=31;
          %Checks if its a leap year and February.
    elseif(month == 2)
        day+= 28;
        if(mod(year,4) == 0)
          day++;
        endif
    else
      day+=30;
    endif
    --month;
  endwhile
endfunction

%Creates the listbox and button for slecting a graph and going back to the previous screen.
function createList() 
  global fh;
  fh = get(groot,'CurrentFigure');
  p = uipanel ("title", "Plots", "position", [.0 .0 1 1]);
  plot_list = uicontrol ("style", "listbox",
                                "units", "normalized",
                                "string", {"Orbit",
                                           "Euler Angles",
                                           "Euler Angles to target to bf",
                                           "Body frame angular rates",
                                           "Magnetorquer Torque",
                                           "Magnetic field",
                                           "Wheel desaturation torque",
                                           "Reaction wheels torque",
                                           "Reaction Wheel speed",
                                           "Actuated and disturbance torques",
                                           "Control mode"
                                           "Sun sensors",
                                           "LDR sensors",
                                           "Triad reconstruction",
                                           "Sensing/Actuating cycle",
                                           "Angle from Nadir of Body Axes",
                                           "Satellite Elevation Angle",
                                           "Ground Station Position in ECEF",
                                           "Ground Station Position in GCI",
                                           "Distance from GS to Satellite"
                                          },
                                "callback", @show_plot,
                                "position", [0.01 0.15 0.37 0.8]);
                                                         
  backButton = uicontrol(
    mainForm =  "style", "pushbutton", "string", "Go Back", "callback", 
                  @goBack, "position", [7 40 50 20]           
    );
  set(fh,'CloseRequestFcn',@closeRequest) 
endfunction

%Call back function for going back to the initial screen.
function goBack(obj, init = false)
  global widgets; 
  global userInput;
  createMainWindow();
  editText();
  disp(userInput)
endfunction

%Loads the selected file.
function show_plot(obj, init = false)
  global dirpath;
  h = guidata (obj);
  index_selected = get(gcbo,'Value');
  
  switch (index_selected)
    case(1)
      h = hgload ([dirpath "simulation_orbit.ofig"]);
    case(2)
      h = hgload ([dirpath "simulation_eulerAngles.ofig"]);
    case(3)
      h = hgload ([dirpath "simulation_eulerAngles_target2bf.ofig"]);
    case(4)
      h = hgload ([dirpath "simulation_w.ofig"]);
    case(5)
      h = hgload ([dirpath "simulation_Tmtq.ofig"]);
    case(6)
      h = hgload ([dirpath "simulation_B_bf.ofig"]);
    case(7)
      h = hgload ([dirpath "simulation_T_c_desat.ofig"]);
    case(8)
      h = hgload ([dirpath "simulation_Trw.ofig"]);
    case(9)
      h = hgload ([dirpath "simulation_w_rw.ofig"]);
    case(10)
      h = hgload ([dirpath "simulation_Ta_Td.ofig"]);
    case(11)
      h = hgload ([dirpath "simulation_controlMode.ofig"]);
    case(12)
      h = hgload ([dirpath "simulation_ss.ofig"]);
      h = hgload ([dirpath "simulation_ss1.ofig"]);
      h = hgload ([dirpath "simulation_ss2.ofig"]);
    case(13)
      h = hgload ([dirpath "simulation_ldr.ofig"]);
    case(14)
      h = hgload ([dirpath "simulation_triad.ofig"]);
    case(15)
      h = hgload ([dirpath "simulation_ASCycle.ofig"]);
    case(16)
      h = hgload ([dirpath "simulation_angleFromNadir.ofig"]);
      h = hgload ([dirpath "simulation_angleFromGS.ofig"]);
    case(17)
      h = hgload ([dirpath "simulation_angleBetweenGroundStationandSatellite.ofig"]);
    case(18)
      h = hgload ([dirpath "simulation_groundStationECEF.ofig"]);
    case(19)
      h = hgload ([dirpath "simulation_groundStationGCI.ofig"]);
    case(20)
      h = hgload ([dirpath  "simulation_groundStationDistance.ofig"]);
    endswitch
endfunction

%Makes a new folder with the time of creation in its name.
function makeFolder()
  global dirpath;
  c = clock;
  folder = "simulation_plots_";
  i = 1;
  while i < length(c)
    folder = strcat([folder], [num2str(c(i))]);
    folder = strcat([folder], "_");
    ++i;
  endwhile
  folder = strcat([folder], [num2str(c(length(c)))]);
  dirpath = strcat(folder, "\\");
  mkdir(folder);
endfunction

createMainWindow();
set(f,'CloseRequestFcn',@closeRequest)