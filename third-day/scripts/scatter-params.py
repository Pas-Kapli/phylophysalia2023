#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_taus(data1,data2):
  # get all columns that start with "tau"  (tau parameters)
  taucols = list(filter(lambda x: x.startswith("tau"), data1.columns.values))

  # get the mean of each column and put them in a dataframe
  tau1_means = data1[taucols].mean()
  tau2_means = data2[taucols].mean()
  tau_means = pd.concat([tau1_means, tau2_means], axis=1, keys=["tau1", "tau2"])

  # plot the means, set equal axes, and save the figure
  plt.scatter(tau_means["tau1"], tau_means["tau2"], color="blue")
  maxval = max(tau_means["tau1"].max(), tau_means["tau2"].max())*1.01
  plt.xlim(0,maxval)
  plt.ylim(0,maxval)
  plt.plot([0,maxval],[0,maxval],color="black",linestyle="dashed")
  plt.title('tau posterior means')
  plt.xlabel(sys.argv[1])
  plt.ylabel(sys.argv[2])
  plt.savefig("taus.pdf", format='pdf')

def plot_thetas(data1,data2):
  # get all columns that start with "theta"  (theta parameters)
  thetacols = list(filter(lambda x: x.startswith("theta"), data1.columns.values))

  # get the mean of each column and put them in a dataframe
  theta1_means = data1[thetacols].mean()
  theta2_means = data2[thetacols].mean()
  theta_means = pd.concat([theta1_means, theta2_means], axis=1, keys=["theta1", "theta2"])

  # plot the means, set equal axes, and save the figure
  plt.scatter(theta_means["theta1"], theta_means["theta2"], color="blue")
  maxval = max(theta_means["theta1"].max(), theta_means["theta2"].max())*1.01
  plt.xlim(0,maxval)
  plt.ylim(0,maxval)
  plt.plot([0,maxval],[0,maxval],color="black",linestyle="dashed")
  plt.title('theta posterior means')
  plt.xlabel(sys.argv[1])
  plt.ylabel(sys.argv[2])
  plt.savefig("thetas.pdf", format='pdf')

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
  plot_taus(data1,data2)
  plot_thetas(data1,data2)
