J/A+A/584/A91   Catalog of dense cores in Aquila from Herschel  (Konyves+, 2015)
================================================================================
A census of dense cores in the Aquila cloud complex: SPIRE/PACS observations
from the Herschel Gould Belt survey.
     Konyves V., Andre P., Men'shchikov A., Palmeirim P., Arzoumanian D.,
     Schneider N., Roy A., Didelon P., Maury A., Shimajiri Y.,
     Di Francesco J., Bontemps S., Peretto N., Benedettini M., Bernard J.-P.,
     Elia D., Griffin M.J., Hill T., Kirk J., Ladjelate B., Marsh K.,
     Martin P.G., Motte F., Nguyen Luong Q., Pezzuto S., Roussel H.,
     Rygl K.L.J., Sadavoy S.I., Schisano E., Spinoglio L., Ward-Thompson D.,
     White G.J.
    <Astron. Astrophys. 584, A91 (2015)>
    =2015A&A...584A..91K        (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: YSOs ; Regional catalog ; Infrared sources ; Interstellar medium ;
              Combined data ; Photometry, millimetric/submm
Keywords: ISM: individual objects: Aquila Rift complex - stars: formation -
          ISM: clouds - ISM: structure - submillimeter: ISM

Abstract:
    We present and discuss the results of the Herschel Gould Belt survey
    (HGBS) observations in an ~11deg^2^ area of the Aquila molecular cloud
    complex at d~260pc, imaged with the SPIRE and PACS photometric
    cameras in parallel mode from 70-micron to 500-micron. Using the
    multi-scale, multi-wavelength source extraction algorithm getsources,
    we identify a complete sample of starless dense cores and embedded
    (Class 0-I) protostars in this region, and analyze their global
    properties and spatial distributions. We find a total of 651 starless
    cores, ~60% +/-10% of which are gravitationally bound prestellar
    cores, and they will likely form stars in the future. We also detect
    58 protostellar cores. The core mass function (CMF) derived for the
    large population of prestellar cores is very similar in shape to the
    stellar initial mass function (IMF), confirming earlier findings on a
    much stronger statistical basis and supporting the view that there is
    a close physical link between the stellar IMF and the prestellar CMF.
    The global shift in mass scale observed between the CMF and the IMF is
    consistent with a typical star formation efficiency of ~40% at the
    level of an individual core. By comparing the numbers of starless
    cores in various density bins to the number of young stellar objects
    (YSOs), we estimate that the lifetime of prestellar cores is ~1Myr,
    which is typically ~4 times longer than the core free-fall time, and
    that it decreases with average core density. We find a strong
    correlation between the spatial distribution of prestellar cores and
    the densest filaments observed in the Aquila complex. About 90% of the
    Herschel-identified prestellar cores are located above a background
    column density corresponding to A_V_~7, and ~75% of them lie within
    filamentary structures with supercritical masses per unit length
    >~16M_{sun}_/pc. These findings support a picture wherein the cores
    making up the peak of the CMF (and probably responsible for the base
    of the IMF) result primarily from the gravitational fragmentation of
    marginally supercritical filaments. Given that filaments appear to
    dominate the mass budget of dense gas at A_V_>7, our findings also
    suggest that the physics of prestellar core formation within filaments
    is responsible for a characteristic "efficiency"
    SFR/M_dense_~5+/-2x10^-8^yr^-1^ for the star formation process in
    dense gas.

Description:
    Based on Herschel Gould Belt survey (Andre et al.,
    2010A&A...518L.102A) observations of the Aquila cloud complex, and
    using the multi-scale, multi-wavelength source extraction algorithm
    getsources (Men'shchikov et al., 2012A&A...542A..81M), we identified a
    total of 749 dense cores, including 685 starless cores and 64
    protostellar cores.

    The observed properties of all dense cores are given in tablea1.dat,
    and their derived properties are listed in tablea2.dat.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat      519      749   Observed properties of dense cores in Aquila
tablea2.dat      178      749   Derived properties of dense cores in Aquila
list.dat         100        2   List of fits images
fits/*             .        2   Individual fits files
--------------------------------------------------------------------------------

See also:
 J/MNRAS/421/3257 : MHO catalogue for Serpens and Aquila (Ioannidis+, 2012)
 J/ApJ/723/915    : BLAST view of Aquila SFR (Rivera-Ingraham+, 2013)

Byte-by-byte Description of file: tablea1.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label        Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---      Seq          Core running number
   5- 19  A15   ---      Name         Core name, HHMMSS.s+DDMMSS, to be added
                                       after HGBS_J
  21- 22  I2    h        RAh          Right ascension (J2000)
  24- 25  I2    min      RAm          Right ascension (J2000)
  27- 31  F5.2  s        RAs          Right ascension (J2000)
      33  A1    ---      DE-          Declination sign (J2000)
  34- 35  I2    deg      DEd          Declination (J2000)
  37- 38  I2    arcmin   DEm          Declination (J2000)
  40- 43  F4.1  arcsec   DEs          Declination (J2000)
  45- 50  F6.1  ---      Signi070     Detection significance at 70um (1)
  52- 60  E9.3  Jy       Sp070        Peak flux density at 70um (in Jy/beam)
  62- 68  E7.2  Jy     e_Sp070        Error on peak flux density at 70um
                                       (in Jy/beam)
  70- 75  F6.2  ---      Sp070/Sbg070 Contrast over local background at 70um
  77- 85  E9.3  Jy       Sconv070     Smoothed peak flux density at 70um
                                       (in Jy/beam500) (2)
  87- 95  E9.3  Jy       Stot070      Integrated flux density at 70um
  97-103  E7.2  Jy     e_Stot070      Error on integrated flux density at 70um
 105-107  I3    arcsec   FWHMa070     ?=-1 Major FWHM diameter at 70um (3)
 109-111  I3    arcsec   FWHMb070     ?=-1 Minor FWHM diameter at 70um (3)
 113-115  I3    deg      PA070        ?=-1 Position angle at 70um (3)(4)
 117-122  F6.1  ---      Signi160     Detection significance at 160um (1)
 124-132  E9.3  Jy       Sp160        Peak flux density at 160um (in Jy/beam)
 134-140  E7.2  Jy     e_Sp160        Error on peak flux density at 160um
                                       (in Jy/beam)
 142-147  F6.2  ---      Sp160/Sbg160 Contrast over local background at 160um
 149-157  E9.3  Jy       Sconv160     Smoothed peak flux density at 160um
                                       (in Jy/beam500) (2)
 159-167  E9.3  Jy       Stot160      Integrated flux density at 160um
 169-175  E7.2  Jy     e_Stot160      Error on integrated flux density at 160um
 177-179  I3    arcsec   FWHMa160     ?=-1 Major FWHM diameter at 160um (3)
 181-183  I3    arcsec   FWHMb160     ?=-1 Minor FWHM diameter at 160um (3)
 185-187  I3    deg      PA160        ?=-1 Position angle at 160um (3)(4)
 189-194  F6.1  ---      Signi250     Detection significance at 250um (1)
 196-204  E9.3  Jy       Sp250        Peak flux density at 250um (in Jy/beam)
 206-212  E7.2  Jy     e_Sp250        Error on peak flux density at 250um
                                       (in Jy/beam)
 214-219  F6.2  ---      Sp250/Sbg250 Contrast over local background at 250um
 221-229  E9.3  Jy       Sconv250     Smoothed peak flux density at 250um
                                       (in Jy/beam500) (2)
 231-239  E9.3  Jy       Stot250      Integrated flux density at 250um
 241-247  E7.2  Jy     e_Stot250      Error on integrated flux density at 250um
 249-251  I3    arcsec   FWHMa250     ?=-1 Major FWHM diameter at 250um (3)
 253-255  I3    arcsec   FWHMb250     ?=-1 Minor FWHM diameter at 250um (3)
 257-259  I3    deg      PA250        ?=-1 Position angle at 250um (3)(4)
 261-266  F6.1  ---      Signi350     Detection significance at 350um (1)
 268-276  E9.3  Jy       Sp350        Peak flux density at 350um (in Jy/beam)
 278-284  E7.2  Jy     e_Sp350        Error on peak flux density at 350um
                                       (in Jy/beam)
 286-291  F6.2  ---      Sp350/Sbg350 Contrast over local background at 350um
 293-301  E9.3  Jy       Sconv350     Smoothed peak flux density at 350um
                                       (in Jy/beam500) (2)
 303-311  E9.3  Jy       Stot350      Integrated flux density at 350um
 313-319  E7.2  Jy     e_Stot350      Error on integrated flux density at 350um
 321-323  I3    arcsec   FWHMa350     Major FWHM diameter of core at 350um
 325-326  I2    arcsec   FWHMb350     Minor FWHM diameter of core at 350um
 328-330  I3    deg      PA350        Position angle of core at 350um (4)
 332-337  F6.1  ---      Signi500     Detection significance at 500um (1)
 339-347  E9.3  Jy       Sp500        Peak flux density at 500um (in Jy/beam)
 349-355  E7.2  Jy     e_Sp500        Error on peak flux density at 500um
                                       (in Jy/beam)
 357-362  F6.2  ---      Sp500/Sbg500 Contrast over local background at 500um
 364-372  E9.3  Jy       Stot500      Integrated flux density at 500um
 374-380  E7.2  Jy     e_Stot500      Error on integrated flux density at 500um
 382-384  I3    arcsec   FWHMa500     Major FWHM diameter of core at 500um
 386-387  I2    arcsec   FWHMb500     Minor FWHM diameter of core at 500um
 389-391  I3    deg      PA500        Position angle of core at 500um (4)
 393-398  F6.1  ---      SigniNH2     Detection significance at column density
 400-404  E5.1 10+21cm-2 NpH2         Peak H2 column density at 18.2" resolution
 406-409  F4.2  ---      NpH2/Nbg     Contrast over local background at
                                       column density
 411-414  E4.1 10+21cm-2 NconvH2      Peak H2 column density at 36.3" resolution
 416-419  E4.1 10+21cm-2 NbgH2        Local background H_2 column density
 421-423  I3    arcsec   FWHMaNH2     Major FWHM diameter of core at N_H2
 425-427  I3    arcsec   FWHMbNH2     Minor FWHM diameter of core at N_H2
 429-431  I3    deg      PANH2        Position angle of core at N_H2 (4)
     433  I1    ---      NSED         [1/5] Number of significant Herschel bands
     435  A1    ---      CSARflag     [012] Associations with CSAR-found
                                             cores (5)
 437-448  A12   ---      Coretype     Core type (6)
 450-482  A33   ---      NSIMBAD      Closest counterpart found in SIMBAD
 484-505  A22   ---      NSPITZER     Closest SPITZER c2d association (7)
 507-519  A13   ---      Com          Comments
--------------------------------------------------------------------------------
Note (1): Detection significance, derived by getsources (Men'shchikov et al.,
           2012A&A...542A..81M), is 0.0 if the core is not visible in clean
           single scales.
Note (2): Peak flux density at the specified wavelength, measured after
          smoothing the data to a 36.3" beam.
Note (3): A special value of -1 is given when no size measurement was possible.
Note (4): Position angle of the core major axis, measured east of north.
Note (5): CSAR-flag: 2 if the getsources core has a counterpart detected by CSAR
           (Kirk, J.M. et al., 2013MNRAS.432.1424K) within 6 arcsec of its peak
           position, 1 if no close CSAR counterpart was found but the peak
           position of a CSAR source lies within the FWHM contour of the
           getsources core in the high-resolution column density map, 0
           otherwise.
Note (6): Core type: starless, prestellar, protostellar.
Note (7): Closest Spitzer-identified YSO from the c2d survey (Dunham et al.,
           2013AJ....145...94D, Allen et al., in prep.) within 6-arcsec of the
           Herschel peak position, if any.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea2.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label     Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---        Seq       Core running number
   5- 19  A15   ---        Name      Core name, HHMMSS.s+DDMMSS,
                                      to be added after HGBS_J*
  21- 22  I2    h          RAh       Right ascension (J2000)
  24- 25  I2    min        RAm       Right ascension (J2000)
  27- 31  F5.2  s          RAs       Right ascension (J2000)
      33  A1    ---        DE-       Declination sign (J2000)
  34- 35  I2    deg        DEd       Declination (J2000)
  37- 38  I2    arcmin     DEm       Declination (J2000)
  40- 43  F4.1  arcsec     DEs       Declination (J2000)
  45- 51  E7.2  pc         Rd        Deconvolved core radius (1)
  53- 59  E7.2  pc         Robs      Observed core radius (2)
  61- 65  F5.2  Msun       Mcore     Estimated core mass
  67- 70  F4.2  Msun     e_Mcore     Uncertainty in the core mass
  72- 75  F4.1  K          Tdust     Dust temperature from SED fitting
  77- 79  F3.1  K        e_Tdust     Uncertainty in the dust temperature
  81- 85  F5.1 10+21cm-2   NH2peak   Peak H2 column density at 36.3" resolution
  87- 91  F5.1 10+21cm-2   NH2av     Average N_H2_ derived with Robs
  93- 97  F5.1 10+21cm-2   NH2avd    Average N_H2_ derived with Rd
  99-103  F5.1 10+4cm-3    nH2peak   Beam-averaged peak volume density
 105-109  F5.1 10+4cm-3    nH2av     Average core volume density from Robs
 111-115  F5.1 10+4cm-3    nH2avd    Average volume density from Rd
 117-120  F4.1  ---        alphaBE   Bonnor-Ebert mass ratio
 122-133  A12   ---        Coretype  Core type (3)
 135-178  A44   ---        Com       Comments (4)
--------------------------------------------------------------------------------
Note (1): Geometrical average between the major and minor FWHM sizes of the core
           [pc], measured in the high-resolution column density map after
           deconvolution from the 18.2-arcsec HPBW resolution of the map.
Note (2): Same as (1) before deconvolution.
Note (3): Core type: starless, prestellar, protostellar.
Note (4): Comments may be "no SED fit", "tentative bound", or "CO high-V_LSR",
          see Sect. 4 of the paper for details.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: list.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  9  F9.5  deg     RAdeg     Right ascension of image center (J2000)
  10- 18  F9.5  deg     DEdeg     Declination of image center (J2000)
      20  I1 arcsec/pix Scale     [3] Scale of the image
  22- 25  I4    ---     Nx        [5233] Number of pixels along X-axis
  27- 30  I4    ---     Ny        [5657] Number of pixels along Y-axis
  32- 37  I6    Kibyte  size      [115642] Size of the fits file
  39- 77  A39   ---     FileName  Name of the fits file in subdirectory fits
  79-100  A22   ---     Title     Title of the fits file
--------------------------------------------------------------------------------

Acknowledgements:
   Vera Konyves, vera.konyves(at)cea.fr
   Philippe Andre, pandre(at)cea.fr

References:
   Andre et al., 2010A&A...518L.102A
   Dunham et al., 2013AJ....145...94D
   Kirk, J.M. et al., 2013MNRAS.432.1424K
   Men'shchikov et al., 2012A&A...542A..81M

================================================================================
(End)   Vera Konyves [CEA/Saclay, France], Patricia Vannier [CDS]    29-Jul-2015
