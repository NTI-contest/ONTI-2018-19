#!/bin/bash

cd src

files=`find ./ -type f | grep -v 'solution.tex' | sort`

for i in ${files}; do
  displayed=`echo ${i} | sed 's#_#\\\\_#g'`
  echo '\textit{\textbf{'${displayed}'}}'

  res_sol=`head -1 ${i} | grep "^pragma" | wc -l`
  res_py=`file ${i} | grep "Python" | wc -l`
  if [ "${res_sol}" == "1" ]; then
    echo '\begin{minted}[fontsize=\footnotesize]{javascript}'
  elif [ "${res_py}" == "1" ]; then
    echo '\begin{minted}[fontsize=\footnotesize]{python}'
  else
    echo '\begin{minted}[fontsize=\footnotesize]'
  fi
  
  cat ${i}
  echo '\end{minted}'
  echo
done
