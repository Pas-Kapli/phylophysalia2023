          seed =  -1

       seqfile = baobab.phy
      Imapfile = baobab.map.txt
       outfile = out.model1.txt
      mcmcfile = mcmc.model1.txt

  speciesdelimitation = 0
         speciestree = 0

   speciesmodelprior = 1  * 0: uniform LH; 1:uniform rooted trees; 2: uniformSLH; 3: uniformSRooted

  species&tree = 6  Adig Agra Agre Amad Arub Smic
                    3 2 1 2 2 1
		    (Smic,(Agre,(Adig,(Arub,(Agra,Amad)e)d)c)b)a;
        phase = 0 0 0 0 0 0
                  
       usedata = 1  * 0: no data (prior); 1:seq like
         nloci = 100  * number of data sets in seqfile

     cleandata = 0    * remove sites with ambiguity data (1:yes, 0:no)?

    thetaprior = 2 0.01 e  # invgamma(a, b) for theta
      tauprior = 3 0.07    # invgamma(a, b) for root tau & Dirichlet(a) for other tau's

      * locusrate = 1 0 0 2 iid
      locusrate = 0
      clock = 1
      * model = hky
      * alphaprior = 2.4 4 4

      finetune =  1: 0.02 0.02 0.02 0.02 0.02 0.02 0.02  # finetune for GBtj, GBspr, theta, tau, mix, locusrate, seqerr
         print = 1 0 0 0   * MCMC samples, locusrate, heredityscalars, Genetrees
        burnin = 5000
      sampfreq = 5
       nsample = 10000

       #threads = 4 1 1
