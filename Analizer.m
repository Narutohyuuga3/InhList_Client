clear all; clc;
myFolder = 'C:\Users\Unseld\Desktop\Unizeugs_WICHTIG\Sem4_WiSe20_21\Bachelorprojekt\WebServer\PyClient\download\';
w=System.IO.FileSystemWatcher(myFolder);
w.EnableRaisingEvents = true;

datalistener =addlistener(w, 'Changed', @DataAvailable);



function DataAvailable(src, event)

    fs = 8000;
    precision = 'int16';
    thisfile= 'keks';
    thisfile = string(event.FullPath); 
   
    fid = fopen(thisfile,'r');               % Open raw pcm file
    audio = int16(fread(fid, Inf, precision));
    fclose(fid);% Convert data to 16 bit
    audio=double(audio);

    N=length(audio);
    max_y = max(abs(audio))*1.1;
    fa = 8000; % Abtastfrequenz
    fn = fa/2; % Nyquistfrequenz
    df = fa/N; % Frequenzauflösung

    %######################


    subplot(4,1,1)
    pspectrum(audio,fs,'spectrogram','Leakage',1,'OverlapPercent',0,'MinThreshold',20,'FrequencyLimits',[1, 4000],'TimeResolution',10e-3);
    [p,f,t] =pspectrum(audio,fs,'spectrogram','Leakage',1,'OverlapPercent',0,'MinThreshold',20,'FrequencyLimits',[1, 2049],'TimeResolution',10e-3);
    title('Frequency-Time-Diagramm')

    %Erstellen und messen der benötigten Params
    %Pre-Exhalation
    lowerFreq_preExh=150;
    upperFreq_preExh=450;
    [t_anfPreExh,t_endPreExh, Result_firstExhalation, Result_firstExhalationsdauer]=readOut(p,lowerFreq_preExh, upperFreq_preExh, 1, 2)
    title('1. Exhalation')

    if(t_anfPreExh>1700 || t_endPreExh > 2500) %Wenn 1. Exhalation nach 10s erst kommt, dann gab es keine
        t_endPreExh=150;
        Result_firstExhalation=0;
        Result_firstExhalationsdauer=0;
    end

    %Inhalation
    lowerFreq_Inh=50;
    upperFreq_Inh=950;
    [t_anfInh,t_endInh, Result_Inhalation, Result_Inhalationsdauer]=readOut(p,lowerFreq_Inh, upperFreq_Inh, t_endPreExh, 3)
    title('Inhalation')

    %Post-Exhalation
    lowerFreq_postExh=150;
    upperFreq_postExh=450;
    [t_anfPostExh,t_endPostExh, Result_secondExhalation, Result_secondExhalationsdauer]=readOut(p,lowerFreq_postExh, upperFreq_postExh, t_endInh, 4)
    title('2. Exhalation')

    %Auswertung
    %innehalten (10s mindestens zwischen Inhalation und 2. Exhalation)
    %Inhalation (langsam & tief: mind. 2s & laut(res>10^6) )
    %Exhalation (gab es eine 1. Exhalation, ueber 1.5s dauer, )

    %%Inhalation
    Ergebnis_Inh=(exp(10^-4*(Result_Inhalation-10^4))+exp(1/1.249*(Result_Inhalationsdauer-1.249)))*100-73.5;
    if(Ergebnis_Inh > 95)
        Ergebnis_Inh=100;
    else
        if(Ergebnis_Inh<15)
            Ergebnis_Inh=0;
        end
    end

    %Innehalten
    Result_Innehalten=exp(0.6*(((t_anfPostExh-t_endInh)/100)-8.999))*100;
    if(Result_Innehalten>95)
        Result_Innehalten=100;
    else
        if(Result_Innehalten<40)
            Result_Innehalten=0;
        end
    end

    %1st Exhalation
    Result_firstExh=exp((Result_firstExhalationsdauer-1.499))*100;
    if(Result_firstExh>95)
        Result_firstExh=100;
    else
        if(Result_firstExh<40)
            Result_firstExh=0;
        end
    end
    disp('Ergebnisse:')
    Ergebnis_Inh
    Result_Innehalten
    Result_firstExh

    filename= erase(thisfile,'C:\Users\Unseld\Desktop\Unizeugs_WICHTIG\Sem4_WiSe20_21\Bachelorprojekt\WebServer\PyClient\download\');
    newname=erase(filename,'.pcm');
    name=newname+'.txt';
    path='C:\Users\Unseld\Desktop\Unizeugs_WICHTIG\Sem4_WiSe20_21\Bachelorprojekt\WebServer\PyClient\upload\'+name;

    disp('*** New analized data coming: ***')
    Result_firstExh
    Ergebnis_Inh
    Result_Innehalten
    Result_akku=69
    
    a=[Ergebnis_Inh; Result_Innehalten; Result_akku; Result_firstExh];
    %encoded_a=unicode2native(a, 'UTF-8');
    %fwrite(fileID, encoded_a, 'uint8')
    %fwrite(fileID, '%d\n', a);
    %fclose(fileID);
    writematrix(a, 'upload\'+name)
    %pause(3);

    %fclose(fileID);
end


function [t_anf, t_end, res, resdauer]=readOut(spectrum, lowerFreq, upperFreq, t_start, subplot_id)
%READOUT Evaluates timestamp and duration from a pspectrum p matrice
    %The folowing code proves if the mean of the frequencies are above 1k
    %for at least 5ms. If this the case, so the phase of inhalation/exhalation is preciding.
    %It measures the start- and end-time of the phase and returns the
    %duration and a result normalized by the frequency-gap
    %
    %t_anf: Phase starts [s]*100
    %t_end: Phase ends [s]*100
    %res: Result sum of vlaues normalized by frequency-gap 
    %resdauer: duration of ohase by time [s]
    
    p_sub=spectrum(lowerFreq:upperFreq,:);
    M=mean(p_sub);
    %V=std(p_sub)./M;
    Anf_bool=0;
    count=0;
    t_anf=1;
    t_end=1;
    poscount=0;
    negcount=0;
    limit=50;
    for i=t_start:1:length(M)
        if(Anf_bool==0)
            if(M(i)>1499)
                poscount=poscount+1;
            else
                negcount=negcount+1;
            end
        else
            if(M(i)<1501)
                poscount=poscount+1;
            else
                negcount=negcount+1;
            end
        end
        count=count+1;
        if(count>=limit)
            if(poscount/count>0.85)
                if(Anf_bool==0)
                    t_anf =i-limit;
                    Anf_bool=1;
                    count=0;
                    poscount=0;
                else
                    t_end =i-limit;
                    break;
                end
            else
                count=0;
                poscount=0;
                negcount=0;
                i=i-(limit-1);
            end
        end
    end
    if (t_end<1)
        t_end=1;
    end
    if(t_anf<1)
        t_anf=1;
    end
    subplot(4,1,subplot_id);
    val=mean(spectrum(lowerFreq:upperFreq,t_anf:t_end));
    t_axis=(t_anf:1:t_end)/100;
    plot(t_axis, val);
    res=sum(val)/(upperFreq-lowerFreq);
    resdauer=(t_end-t_anf)/100;
end