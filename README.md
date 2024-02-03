# bandwizard
QGIS plugin for visualizing raster bands and changing their order

This is a python based QGIS plugin. Tested on Ubuntu 20.04, QGIS 3.22 Desktop.

Multispectral rasters have various band/channels, most commonly the red, green, blue and NIR. Imagery providers often arrange bands in either RGBI or BGRI order. QGIS provides a powerful interface to set the order of individual channels. This plugin enables setting the most common BGRI and RGBI orders with a click of a button. It also allows inspecting the individual bands as grayscale. This is particularly useful when using multipolar SAR imagery. The interface is intuitive, and an advanced settings button allows accessing the QGIS interface quickly.

The Plugin can identify rasters and ignores vectors. It can find the number of bands available in the raster. It used the default contrast settings applicable on the raster.

How to install:
* Download the git as zip file.
* Use the menu: ``Plugins`` > ``Mange and install plugins``
* On the options available on the left, choose ``Install from ZIP file``
* Browse and select the downloaded bandwizard.zip file
* After installation, the ``Raster`` menu should show the ``BandWizard`` option
* If toolbars are enabled, the BandWizard icon should be visible

Usage:
* Click on the toolbar OR select in the menu ``Raster`` > ``BandWizard`` > ``Raster Band Wizard``
* The BandWizrd dockable widget should appear on the top edge 
* Open a raster file and click on the layer
* For rasters, the widget will display number of rasters and enable the required buttons
* For vectors, the widget will display ``Not Raster``
* For PAN or single channel intensity images, RGBI and BGRI options are not applicable
* For Multichannel images such as MX, PSNC, etc, the RGBI and BGRI buttons are available
* Click on ``Adv Settings`` button to access finer controls offered by QGIS

Dependencies:
There are absolutely no dependencies on additional python packages other than those shipped with QGIS.

