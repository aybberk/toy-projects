
function varargout = ppp(varargin)
% PPP MATLAB code for ppp.fig
%      PPP, by itself, creates a new PPP or raises the existing singleton*.
%
%      H = PPP returns the handle to a new PPP or the handle to the
%      existing singleton*.
%
%      PPP('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in PPP.M with the given input arguments.
%
%      PPP('Property','Value',...) creates a new PPP or raises the existing
%      singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before ppp_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property
%      application stop.  All inputs are passed to ppp_OpeningFcn via
%      varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help ppp

% Last Modified by GUIDE v2.5 18-Dec-2016 11:46:58

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @ppp_OpeningFcn, ...
    'gui_OutputFcn',  @ppp_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before ppp is made visible.
function ppp_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn. hObject    handle to
% figure eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA) varargin
% command line arguments to ppp (see VARARGIN)

% Choose default command line output for ppp
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes ppp wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = ppp_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT); hObject
% handle to figure eventdata  reserved - to be defined in a future version
% of MATLAB handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


function pushbutton1_Callback(hObject, eventdata, handles)
path(path,'C:\Users\user\Desktop\ipod')
path(path,'C:\Users\user\Desktop')
global audionamemp3;
global ses;
global Fs;
[ses,Fs]=audioread(audionamemp3);
assignin('base','ses',ses);


function edit1_Callback(hObject, eventdata, handles)
global audionamemp3;
global audioname;
audioname=get(hObject,'String');
audionamemp3=[get(hObject,'String'),'.mp3'];


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO) eventdata  reserved - to be defined
% in a future version of MATLAB handles    empty - handles not created
% until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
global sesnovocals;
global Fs;
sound(sesnovocals,Fs);
% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO) eventdata  reserved - to be
% defined in a future version of MATLAB handles    structure with handles
% and user data (see GUIDATA)
clear sound;

% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO) eventdata  reserved - to be
% defined in a future version of MATLAB handles    structure with handles
% and user data (see GUIDATA)
global ses;
global sesnovocals;
y1=ses(:,1);
if isvector(ses)==0
    y2=ses(:,2);
    
end

sesnovocals=(y1-y2)/2;
assignin('base','sesnovocals',sesnovocals);




% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
global audioname;
global sesnovocals;
global Fs;
audiowrite([audioname,['.mp4']],sesnovocals,Fs,'Bitrate',128);


% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
global ses;
global Fs;
sound(ses,Fs);
