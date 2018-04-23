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
if(~(size(y,1)==1 || size(y,2)==1))
ses=(y(:,1)+y(:,2))';%2 kanallin ortalamasini al%
else ses=y';
end
% ses=(y(:,1)-y(:,2))'; %vocal reduction
m=numel(ses); %sesin eleman sayisi%
sure=m/Fs;  %süre%
windowpower=13;
L_window=2^windowpower;  %window uzunlugu 2^n for efficiency
overlapfactor=5;  %bir windowun 1-1/overlapfactor luk k?sm? digeriyle overlap oluyo
overlap=100*(overlapfactor-1)/overlapfactor;
% L_window=round(kacmsdebir*Fs/(1000-10*overlap)); %yepyeni window uzunlugu
kacmsdebir=L_window*(1000-10*overlap)/(Fs);
snyibol=1000/kacmsdebir;
herwindow=(L_window/Fs);
tanewindow=round((m/L_window-1)/(1-overlap/100));
kacabolecezz=4;
% % % % overlap_seyi1=200;
% % % % factor=(2*overlap_seyi+100)/200; %windowlength faktörü. küçüldükçe precision azalir hiz artar (1'den küçük 0'dan büyük olacak)
fprintf('her window %d sample ve %.2f saniye \nwindowlar arasinda  %.1f%% overlap var \ntoplam %d civari window olacak\n\n',L_window, herwindow, overlap, tanewindow);
fprintf('%d tane %d-point FFT alinacak\n\n',tanewindow,L_window);
fprintf('bolup kirptiktan sonra %d x %d matrix olusacak\n\n',tanewindow,round(L_window/(kacabolecezz*2))); 
    
dvm=input('devam?');

disp('Analyzing the sound...');

%% window %%
% window
        wind=hamming(L_window)';
        windowww='hamin';
        
%% FFT %%
% yukaridaki parametrelere gore sesin stftsini alir ve hepsini alt alta
% dizip bir matris olusturur(her satir bir instant)

disp('Obtaining Spectrogram...'); 
b=zeros(tanewindow,L_window); 
tic
for n=1/snyibol  :  1/snyibol  :  sure-herwindow;   
    b(round(snyibol*n),:)=((fft((ses((round(Fs*(n-1/snyibol))+1):round(Fs*(n-1/snyibol))+L_window).*wind)))); 
end
toc
%% phasomatrix&absomatrix /w normalization&kirpma
%% freqs tanim, tepeden kirpma, absomatrix, phasomatrix %%

% 1. spectrogram cizimi icin frekans eksenini tanimlar
% 2. sarkilarda pek gorulmeyen yuksek frekanslari ihtiyacimiz olmadigi icin
% kirpar boylece isler kolaylasir, comp. time azal?r, ayni zamanda
% spectrogram gorsel olarak daha anlamli olur.

kacabolecez=kacabolecezz;
freqs=linspace(0,(Fs-Fs/L_window)/(2*kacabolecez) ,floor((L_window/(2*kacabolecez)))); 
% freqs=linspace(0,floor((L_window/(2*kacabolecez)))-1,floor((L_window/(2*kacabolecez)))); %kontrol amacli freqs

b=b(:,1:length(freqs));

phasomatrix=angle(b);
absomatrix=abs(b);

%% downlimit&logo
downlimit=1e-3;
absomatrix(absomatrix<=downlimit)=downlimit; 
logomatrix=20*log10(absomatrix);
%% normalization 
% kontrolzero=ones(1,size(absomatrix,2));
% for n=1:size(absomatrix,1);
%     if absomatrix(n,:)~=downlimit*kontrolzero
%     absomatrix(n,:)= absomatrix(n,:)/max(absomatrix(n,:));
%     end
% end
% absomatrix(absomatrix<=downlimit)=downlimit; %bi daha yaptik asil amaciyle


%% time tanim %%
% spectrogram cizimi icin zaman eksenini tanimlar
timetanim=numel(absomatrix(:,1));
time=linspace(herwindow,sure+herwindow,timetanim);
% time=linspace(0,timetanim-1,timetanim); %kontrol amacli time


%% cizim absomatrix %%
% figure('units','normalized','outerposition',[0 0 1 1])
% imagesc(time,freqs,absomatrix')
% xlabel('Time(s)');
% ylabel('Frequency(Hz)');
% ylabel(colorbar,'Magnitude');
% set(gca,'YDir','normal')
% title(['Spectrogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',...
%     num2str(overlap),'% overlap and using ',windowww,' Window'])
% colormap(hot);

%% cizim logomatrix

figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,freqs,logomatrix')
xlabel('Time(s)');
ylabel('Frequency(Hz)');
ylabel(colorbar,'Magnitude');
set(gca,'YDir','normal')
title(['Spectrogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',...
    num2str(overlap),'% overlap and using ',windowww,' Window'])
colormap(hot);

%% percussive filter %%%% pitch filter %%
% 
% disp('Filtering percussive events...'); 
% tic
% filterorder=30;
% p=2;
% times=1;
% for n=1:times
% percfiltedabsomatrix=medfilt1(absomatrix,filterorder,size(absomatrix,1),1); %size1=time=time impulse filter
% pitchfiltedabsomatrix=medfilt1(absomatrix,filterorder,size(absomatrix,2),2); %size2=frequency
% pitchelements=percfiltedabsomatrix.^p./(percfiltedabsomatrix.^p+pitchfiltedabsomatrix.^p);
% percelements=pitchfiltedabsomatrix.^p./(percfiltedabsomatrix.^p+pitchfiltedabsomatrix.^p);
% absomatrix=pitchelements.*absomatrix;
% end
% downlimit=1e-3;
% absomatrix(absomatrix<=downlimit)=downlimit; 
% logomatrix=20*log10(absomatrix);
% toc


%% cizim logomatrix filtered

figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,freqs,logomatrix')
xlabel('Time(s)');
ylabel('Frequency(Hz)');
ylabel(colorbar,'Magnitude');
set(gca,'YDir','normal')
title(['Spectrogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',...
    num2str(overlap),'% overlap and using ',windowww,' Window'])
colormap(hot);

%% cizim phasomatrix %%
% figure('units','normalized','outerposition',[0 0 1 1])
% imagesc(time,freqs,phasomatrix')
% xlabel('Time(s)');
% ylabel('Frequency(Hz)');
% ylabel(colorbar,'Phase');
% set(gca,'YDir','normal')
% title(['Phasogram of ',filename,' for every ',num2str(1000/snyibol),' miliseconds with ',...
%     num2str(overlap),'% overlap and using ',windowww,' Window'])
% colormap(hot);

%% surf cizimi %% 
% sizec=size(c);
% freqssurf=linspace(Fs/L_window,Fs/kacabolecez,size(c,2)); 
% timesurf=linspace(herwindow,sure+herwindow,size(c,1));
% figure('units','normalized','outerposition',[0 0 1 1])
% h=surf(timesurf,freqssurf,absomatrix');
% set(h,'LineStyle','none')
% xlabel('Time(s)');
% ylabel('Frequency(Hz)');
% zlabel('Magn itude')
% view(-25,75);
% colormap(hot);

%% harmonic extraction %%
% % enstrumanlarin dogasi geregi icinde bulunan ses harmoniklerini siler

h_coef=1;
cfilted=absomatrix;
disp('Filtering Harmonics...');
tic
    for n1=1:size(absomatrix,1) %for all times%
        for n2=size(absomatrix,2)-1:-1:1 %for all freqs%
            if absomatrix(n1,n2)==downlimit
            continue;
            else
                for n3=[3,5,7] %her harmonici icin kontrol%
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
colormap(hot);
absomatrix=cfilted;

%% IFFT from absomatrix/logomatrix and phasomatrix 
% oynat=[];
% while isempty(oynat)||oynat~=1&&oynat~=2
% oynat=input('Oynat? (1/2)\n','s');
% oynat=str2double(oynat);
% if oynat==1 %%
% disp('Resynthesising the audio...'); 
% tic
% absomatrixtekrar=10.^(logomatrix/20);
% sestekrar=zeros(1,ceil(sure)*Fs);
% fftmatrix=zeros(tanewindow,L_window);
% fftmatrix(:,1:size(absomatrixtekrar,2))=absomatrixtekrar.*(cos(phasomatrix)+1j*sin(phasomatrix));
% for n=1:size(absomatrixtekrar,1)
% sestekrar(floor(L_window/overlapfactor)*(n-1)+1:floor(L_window/overlapfactor)*(n-1)+L_window)=sestekrar(floor(L_window/overlapfactor)*(n-1)+1:floor(L_window/overlapfactor)*(n-1)+L_window)+ifft(fftmatrix(n,:)).*(1./wind);
% end
% 
% end
% sestekrar=real(sestekrar);
% sound(sestekrar,Fs);
% end
% toc

%% piano %%
%%%%sesi piyano tuslarina doker

disp('Notesaver..');
tic
ilknota=log10(27.5);                         % a0=27.5 hz
sonnota=log10(4186.01);                       % c8=4186.01 hz
notalar=logspace(ilknota,sonnota,88); %notalar(n)=88-key piyanonun n. tusunun frekans?
notalar=notalar(1:88);
keysayisi=numel(notalar);
keyler=zeros(1,keysayisi);
piano=downlimit*ones(size(absomatrix,1),keysayisi);
for n1=1:size(absomatrix,1)
    for n2=1:size(absomatrix,2)        
        if absomatrix(n1,n2) > downlimit;
            [value2,index2]=min(abs(notalar-freqs(n2)));
            piano(n1,index2)=piano(n1,index2)+(absomatrix(n1,n2)); %lin icin
           
        end
    end
end
toc

figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,linspace(1,keysayisi,keysayisi),piano')
xlabel('Time(s)');
ylabel('Piyano Tusu');
% ylabel(colorbar,'Power/frequency(dB/Hz)')
set(gca,'YDir','normal')
colormap(hot)

 %% harmonic extraction for piano %%
% % harmonikleri piyanoya dokulmus sarkida siler
% 
% harmonicsemitones=[0 12 19 24 28 31 34 36];
% h_coef=1; %%% lin icin
% pianofilted=piano;
% disp('Filtering Harmonics in Notesaver...');
% tic
%     for n1=1:size(piano,1) %for all times%
%         for n2=size(piano,2):-1:1 %for all tus%
%             if piano(n1,n2)==downlimit
%             continue;
%             else
%                 for n3=7:-1:2 %her harmonici icin kontrol%
%                     if harmonicsemitones(n3)>=n2
%                         continue
%                     end
%                     kontrol=h_coef^n*piano(n1,n2);
%                     if  piano(n1,n2-harmonicsemitones(n3))>=kontrol
%                     pianofilted(n1,n2)=downlimit; %downlimite esitledik
%                     end                 
%                 end
%             end
%         end 
%     end
% toc
% figure('units','normalized','outerposition',[0 0 1 1])
% imagesc(time,linspace(1,keysayisi,keysayisi),pianofilted')
% xlabel('Time(s)');
% ylabel('Piyano Tusu');
% % ylabel(colorbar,'Power/frequency(dB/Hz)')
% set(gca,'YDir','normal')
% title('Notesaver(Filted)');
% colormap(hot);
% piano=pianofilted;

% piano to one octave(chromagram) %%
% her andaki nota yogunluklar?n? oktavdan bag?ms?z halde bulur (12 nota)

   chromagram=zeros(size(piano,1),12);
   for n1=1:size(piano,1) %tum zamanlar
       for n2=1:size(piano,2)
           chromagram(n1,mod(n2,12)+1)=chromagram(n1,mod(n2,12)+1)+piano(n1,n2);
       end
   end
   
   temp=chromagram(:,1);
   chromagram(:,1)=[];
   chromagram(:,12)=temp;
   clear temp;
   
figure('units','normalized','outerposition',[0 0 1 1])
imagesc(time,linspace(1,12,12),chromagram')
set(gca, 'YTick', 1:12, 'YTickLabel', {'A' 'A#' 'B' 'C' 'C#' 'D' 'D#' 'E' 'F' 'F#' 'G' 'G#'});
ylabel(colorbar,'Power/frequency(dB/Hz)')
title('Chromagram');
set(gca,'YDir','normal')
colormap(hot)

% chordagram %%
% % % her andaki akor yogunluklarini bulur 
chordgram=zeros(size(chromagram,1),24);
for n1=1:size(chromagram,1)
    for n2=1:12
        temp=mod([2*(n2-1)+1,2*(n2-1)+2,2*(n2-1)+11,2*(n2-1)+12,2*(n2-1)+18,2*(n2-1)+19],24);
        temp(temp==0)=24;
    chordgram(n1,temp)=chordgram(n1,temp)+chromagram(n1,n2);
   
    end
end

tolerance=0.5;
for n1=1:size(chordgram,1)
    
    if max(chordgram(n1,:))<tolerance
        chordgram(n1,:) = 0;
        continue
    end
    chordgram(n1,:) = chordgram(n1,:)/max(chordgram(n1,:));
end

figure('units','normalized','outerposition',[0 0 1 1])
title('Chords');
imagesc(time,linspace(1,24,24),chordgram')
set(gca, 'YTick', 1:24, 'YTickLabel', {'Am' 'A' 'A#m' 'A#' 'Bm' 'B' 'Cm' 'C' 'C#m' 'C#' 'Dm' 'D' 'D#m' 'D#' 'Em' 'E' 'Fm' 'F' 'F#m' 'F#' 'Gm' 'G' 'G#m' 'G#'});
colormap(hot);
drawnow;

% %% playback %%
% pause(2);
% baslangic=0;
% bitis=sure;
% sound(ses(round(Fs*baslangic)+1:floor(Fs*bitis)),Fs);


