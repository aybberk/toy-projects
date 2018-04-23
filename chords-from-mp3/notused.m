%% kayit&okuma %%
%kullanici girisine gore ses kaydeder veya mp3 okur
close all;
clear variables; 
clear sound;
path(path,'C:\Users\user\Desktop\ipod');
path(path,'C:\Users\user\Desktop');
path(path,'C:\Users\user\Desktop\ipod\piano-classical');
readrecord=[];
while isempty(readrecord)||readrecord~=1&&readrecord~=2
readrecord=input('Read or Record? (1/2)\n','s');
readrecord=str2double(readrecord);
end

if readrecord==1 %%
    filename=input('File name?\n','s');
    filename=[filename '.mp3'];
    [y,Fs]=audioread(filename); 
end

if readrecord==2 %%recorder%%
            kayitsuresi=[];
            while isempty(kayitsuresi)||kayitsuresi<1||kayitsuresi>60
            kayitsuresi=input('Record duration?(1-60)\n');
            end
            Fs_rec=44100;
            recObj = audiorecorder(Fs_rec,16,1);
       
            disp('Record started.')
            recordblocking(recObj, kayitsuresi);
            disp('Record finished.');
            y = getaudiodata(recObj);
            Fs=Fs_rec;
            filename='the recording';
end                  


%% isleme %%
% overlap factor ve window uzunluklariyla alinacak STFT'nin parametrelerini
% belirler

ses=y(:,1)';%1. channeli al%
% ses=(y(:,1)-y(:,2))'; %vocal reduction
m=numel(ses); %sesin eleman sayisi%
sure=m/Fs;  %süre%
windowpower=14;
L_window=2^windowpower;  %window uzunlugu 2^n for efficiency
overlapfactor=10;  %bir windowun 1-1/overlapfactor luk k?sm? digeriyle overlap oluyo
overlap=100*(overlapfactor-1)/overlapfactor;
% L_window=round(kacmsdebir*Fs/(1000-10*overlap)); %yepyeni window uzunlugu
kacmsdebir=L_window*(1000-10*overlap)/(Fs);
snyibol=1000/kacmsdebir;
herwindow=(L_window/Fs);
tanewindow=round((m/L_window-1)/(1-overlap/100));
% % % % overlap_seyi1=200;
% % % % factor=(2*overlap_seyi+100)/200; %windowlength faktörü. küçüldükçe precision azalir hiz artar (1'den küçük 0'dan büyük olacak)
fprintf('her window %d sample ve %.2f saniye \nwindowlar arasinda  %.1f%% overlap var \ntoplam %d civari window olacak\n\n',L_window, herwindow, overlap, tanewindow);
fprintf('%d tane %d-point FFT alinacak\n\n',tanewindow,L_window);
    
dvm=input('devam?');

disp('Analyzing the sound...');

ses=conv(ses,ses);