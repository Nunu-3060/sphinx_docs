付録 D 参考文献
==================================================

教科書
------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 文献
     - 内容
   * - A. V. Oppenheim and R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Pearson, 2010.
     - 離散時間信号処理の標準的な教科書。本書で扱った内容のほぼすべてを、証明を含めて詳しく扱っている。
   * - J. H. McClellan, R. W. Schafer, and M. A. Yoder, *DSP First*, 2nd ed., Pearson, 2016.
     - 正弦波と周波数応答から始める入門書。正規化角周波数 :math:`\hat{\omega}` の表記は、この本にならった。
   * - R. G. Lyons, *Understanding Digital Signal Processing*, 3rd ed., Prentice Hall, 2010.
     - 数式を抑え、図と具体例で説明する実践的な入門書。
   * - S. W. Smith, *The Scientist and Engineer's Guide to Digital Signal Processing*, California Technical Publishing, 1997.
     - 実務家向けの入門書。全文が著者のウェブサイト https://www.dspguide.com/ で公開されている。
   * - E. O. Brigham, *The Fast Fourier Transform and Its Applications*, Prentice Hall, 1988.
     - FFT とその応用を、フーリエ変換との関係から詳しく説明している。
   * - J. O. Smith III, *Mathematics of the Discrete Fourier Transform (DFT), with Audio Applications*, 2nd ed., W3K Publishing, 2007.
     - 複素数から DFT までの数学を、音響の応用とともに丁寧に説明している。

論文
----

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 文献
     - 内容
   * - C. E. Shannon, "Communication in the presence of noise," *Proceedings of the IRE*, vol. 37, no. 1, pp. 10--21, 1949.
     - 標本化定理を明確に示した論文（第 4 章）。
   * - J. W. Cooley and J. W. Tukey, "An algorithm for the machine calculation of complex Fourier series," *Mathematics of Computation*, vol. 19, no. 90, pp. 297--301, 1965.
     - FFT を広く知らしめた論文（第 7 章）。
   * - F. J. Harris, "On the use of windows for harmonic analysis with the discrete Fourier transform," *Proceedings of the IEEE*, vol. 66, no. 1, pp. 51--83, 1978.
     - 窓関数の特性を網羅的に比較した論文。:numref:`table-ch08-windows` の値の出典である（第 8 章）。
   * - P. D. Welch, "The use of fast Fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms," *IEEE Transactions on Audio and Electroacoustics*, vol. AU-15, no. 2, pp. 70--73, 1967.
     - ウェルチ法の論文（第 8 章）。
   * - G. Goertzel, "An algorithm for the evaluation of finite trigonometric series," *The American Mathematical Monthly*, vol. 65, no. 1, pp. 34--35, 1958.
     - ゲルツェル法の論文（第 10 章）。

規格とドキュメント
------------------

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 文献
     - 内容
   * - ITU-T Recommendation Q.23, *Technical features of push-button telephone sets*, 1988.
     - DTMF 信号の周波数の割り当てを定めた規格（第 10 章）。
   * - NumPy Developers, "Discrete Fourier Transform (numpy.fft)," https://numpy.org/doc/stable/reference/routines.fft.html
     - NumPy の FFT 関数のリファレンス。正規化の定義などが説明されている（第 7 章）。
   * - SciPy Developers, "Signal processing (scipy.signal)," https://docs.scipy.org/doc/scipy/reference/signal.html
     - SciPy の信号処理の関数のリファレンス（第 8 章、第 9 章、第 10 章）。
   * - SciPy Developers, "Fourier Transforms (scipy.fft)," https://docs.scipy.org/doc/scipy/reference/fft.html
     - SciPy の FFT 関数のリファレンス（第 7 章）。
