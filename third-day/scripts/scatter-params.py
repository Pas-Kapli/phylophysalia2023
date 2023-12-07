#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_data(data1,data2,param_prefix,title,savefile):
  # get all columns that start with "tau"  (tau parameters)
  cols = list(filter(lambda x: x.startswith(param_prefix), data1.columns.values))
  if len(cols) == 0:
    return

  # get the mean of each column and put them in a dataframe
  means1 = data1[cols].mean()
  means2 = data2[cols].mean()
  all_means = []
  all_means = pd.concat([means1, means2], axis=1, keys=["key1", "key2"])

  # plot the means, set equal axes, and save the figure
  plt.scatter(all_means["key1"], all_means["key2"], color="blue")
  maxval = max(all_means["key1"].max(), all_means["key2"].max())*1.01
  plt.xlim(0,maxval)
  plt.ylim(0,maxval)
  plt.plot([0,maxval],[0,maxval],color="black",linestyle="dashed")
  plt.title(title)
  plt.xlabel(sys.argv[1])
  plt.ylabel(sys.argv[2])
  plt.savefig(savefile, format='pdf')
  plt.close("all")

def read_data(filename1,filename2):
  data1 = pd.read_table(filename1, delim_whitespace=True)
  data2 = pd.read_table(filename2, delim_whitespace=True)

  return data1,data2

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " mcmcfile1 mcmcfile2")
    sys.exit(0)

  # read each mcmc files into a dataframe
  data1, data2 = read_data(sys.argv[1],sys.argv[2])

  # create scatterplots for taus and thetas
  plot_data(data1,data2,"phi","phi posterior means","phis.pdf")
  plot_data(data1,data2,"tau","tau posterior means","taus.pdf")
  plot_data(data1,data2,"theta","theta posterior means","thetas.pdf")
