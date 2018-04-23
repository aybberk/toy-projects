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
windowpower=15;
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


%% window %%
% window
        wind=hamming(L_window)';
        windowww='bohman';
        
        
%% FFT %%
% yukaridaki parametrelere gore sesin stftsini alir ve hepsini alt alta
% dizip bir matris olusturur(her satir bir instant)

disp('Obtaining Fourier Transform...'); 
b=zeros(tanewindow,L_window);
tic
for n=1/snyibol  :  1/snyibol  :  sure-herwindow;   
    b(round(snyibol*n),:)=((fft((ses((round(Fs*(n-1/snyibol))+1):round(Fs*(n-1/snyibol))+L_window).*wind)))); 
end
toc
%% phasomatrix&absomatrix
absomatrix=abs(b);
phasomatrix=angle(b);
%% freqs tanim, tepeden kirpma %%
% 1. spectrogram cizimi icin frekans eksenini tanimlar
% 2. sarkilarda pek gorulmeyen yuksek frekanslari ihtiyacimiz olmadigi icin
% kirpar boylece isler kolaylasir, comp. time azal?r, ayni zamanda
% spectrogram gorsel olarak daha anlamli olur.

kacabolecez=8;
freqs=linspace(0,(Fs-Fs/L_window)/(2*kacabolecez) ,floor((L_window/(2*kacabolecez)))); 
% freqs=linspace(0,floor((L_window/(2*kacabolecez)))-1,floor((L_window/(2*kacabolecez)))); %kontrol amacli freqs
absomatrix=absomatrix(:,1:length(freqs)); 
phasomatrix=phasomatrix(:,1:length(freqs));



%% time tanim %%
% spectrogram cizimi icin zaman eksenini tanimlar
timetanim=numel(b(:,1));
time=linspace(herwindow,sure+herwindow,timetanim);

% time=linspace(0,timetanim-1,timetanim); %kontrol amacli time
%% cizimmag %%
figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,freqs,absomatrix')
xlabel('Time(s)');
ylabel('Frequency(Hz)');
ylabel(colorbar,'Magnitude');
set(gca,'YDir','normal')
title(['Spectrogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',...
    num2str(overlap),'% overlap and using ',windowww,' Window'])
colormap(jet);
%% cizimphase %%
figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,freqs,phasomatrix')
xlabel('Time(s)');
ylabel('Frequency(Hz)');
ylabel(colorbar,'Phase');
set(gca,'YDir','normal')
title(['Phasogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',...
    num2str(overlap),'% overlap and using ',windowww,' Window'])
colormap(jet);
%% harmonic extraction %%
% % % enstrumanlarin dogasi geregi icinde bulunan ses harmoniklerini siler
downlimit=0;
h_coef=1;
cfilted=absomatrix;
disp('Filtering Harmonics...');
tic
    for n1=1:size(absomatrix,1) %for all times%
        for n2=size(absomatrix,2)-1:-1:1 %for all freqs%
            if absomatrix(n1,n2)==downlimit
            continue;
            else
                for n3=[3,5] %her harmonici icin kontrol%
                    if floor((n2-1)/n3-3)>0
                    kontrol=h_coef^n*absomatrix(n1,n2);
                    if    ... %c(n1,n2) harmonic miymis
                    absomatrix(n1,floor((n2-1)/n3  ))>= kontrol...
                  ||absomatrix(n1,floor((n2-1)/n3-1))>= kontrol...
                  ||absomatrix(n1,floor((n2-1)/n3+1))>= kontrol...
                  ||absomatrix(n1,floor((n2-1)/n3-2))>= kontrol...
                  ||absomatrix(n1,floor((n2-1)/n3+2))>= kontrol...
                  ||absomatrix(n1,floor((n2-1)/n3-3))>= kontrol...         
                  ||absomatrix(n1,floor((n2-1)/n3+3))>= kontrol 

                cfilted(n1,n2)=downlimit; %downlimite esitledik
                    end    
                    end
                end
            end
        end 
    end
toc
figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,freqs,cfilted')
xlabel('Time(s)');
ylabel('Frequency(Hz)');
ylabel(colorbar,'Magnitude');
set(gca,'YDir','normal')
title(['CFILTED Spectrogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',num2str(overlap),'% overlap and using ',windowww,' Window'])
colormap(jet);
absomatrix=cfilted;
%% IFFT from absomatrix and phasomatrix
sestekrar=zeros(1,sure*Fs);
fftmatrix=zeros(tanewindow,L_window);
fftmatrix(:,1:size(absomatrix,2))=absomatrix.*(cos(phasomatrix)+1j*sin(phasomatrix));
for n=1:size(absomatrix,1)
sestekrar(round(L_window/overlapfactor)*(n-1)+1:round(L_window/overlapfactor)*(n-1)+L_window)=sestekrar(round(L_window/overlapfactor)*(n-1)+1:round(L_window/overlapfactor)*(n-1)+L_window)+ifft(fftmatrix(n,:)).*(1./wind);
sestekrar=real(sestekrar);
end