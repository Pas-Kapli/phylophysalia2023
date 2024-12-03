          seed =  -1

       seqfile = ../../../../baobab/baobab.phy
      Imapfile = ../../../../baobab/baobab.map.txt
       jobname = model2

  speciesdelimitation = 0
         speciestree = 0

#   speciesmodelprior = 1      # 0: uniform LH; 1:uniform rooted trees; 2: uniformSLH; 3: uniformSRooted

  species&tree = 6  Adig Agra Agre Amad Arub Smic
                    3 2 1 2 2 1
                  (Smic, (Agre,((x[&phi=0.200000,tau-parent=no],Adig)w,(Arub,((Agra)x[&phi=0.800000,tau-parent=yes],Amad)e)d)c)b)a;
        phase = 0 0 0 0 0 0
                  
       usedata = 1             # 0: no data (prior); 1:seq like
         nloci = 100           # number of data sets in seqfile

     cleandata = 0             # remove sites with ambiguity data (1:yes, 0:no)?

    thetaprior = gamma 3 300   # Gamma(a, b) for theta
      tauprior = gamma 3 85    # Gamma(a, b) for root tau
      phiprior = 1 1           # Beta(a,b)

      locusrate = 0
      clock = 1 

	 finetune =  1: 0.02 0.02 0.02 0.02 0.02 0.02 0.02 0.02
         print = 1 0 0 0       # MCMC samples, locusrate, heredityscalars, Genetrees
        burnin = 5000
      sampfreq = 5
       nsample = 10000

       #threads = 4 1 1
