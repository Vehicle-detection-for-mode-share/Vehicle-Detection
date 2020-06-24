[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU License][license-shield]][license-url]

[![Contributors](https://img.shields.io/github/contributors/Vehicle-detection-for-mode-share/Vehicle-Detection.svg)](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/contributors)
[![Forks](https://img.shields.io/github/forks/Vehicle-detection-for-mode-share/Vehicle-Detection.svg)](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/forks)
[![GitHub Stars](https://img.shields.io/github/stars/Vehicle-detection-for-mode-share/Vehicle-Detection.svg)](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/Vehicle-detection-for-mode-share/Vehicle-Detection.svg)](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/issues)
[![GNU License][license-shield]][license-url]


# Vehicle Detection for Google Street View Images: Characterizing Mode Share Using Computer Vision

The objectives of this project are two-fold:

1. Create, train, test and tune a deep learning model to achieve high sensitivity and specificity for counting vehicles in Google Street View images
2. Use the model to count vehicles across several major cities in the World

## Research Output :postbox:

So far, this project has potential for the following outputs:

1. GSV vehicle counts ranking of 73 cities for motorcycling and cycling
2. Detailed comparison: GSV vehicle counts versus control travel or census data for motorcycling and cycling in a small number of cities

## Getting Started :rocket:

Here is a list of the items contained in this repository:

- **[Data-Preparation](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/tree/master/Data-Preparation)**: folder containing code for the data preparation process

- **[Model-Build](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/tree/master/Model-Build)**: folder containing code for the creation, training and tuning process of the deep learning model

- **[Mode-Share](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/tree/master/Mode-Share)**: folder containing statistical analyses assessing model's ability to characterize mode share

## Outstanding Issues :warning:

:heavy_check_mark: Vehicle Classes: defining main vehicle classes

:heavy_multiplication_x: Radius: current equation might not capture all appropriate neighbourhoods in certain cities, depending on city density

:heavy_multiplication_x: Vehicle Classes: reviewing edge cases to redefine final vehicle classes

:heavy_multiplication_x: Image Overlap: code needs to be written to delete continuous frames to prevent multiple counts of same vehicle

## Contributing :pencil:

Contributions are what make the open source community a great place to learn, inspire, and create. Any contributions you make are appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingContribution`)
3. Commit your Changes (`git commit -m 'Add some AmazingContribution'`)
4. Push to the Branch (`git push origin feature/AmazingContribution`)
5. Open a Pull Request

## Reporting Issues :open_file_folder:

Does something seem off? Make sure to [report it](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/issues).

## License :clipboard:

Distributed under the GNU Affero General Public License. See [LICENSE](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/blob/master/LICENSE) for more information.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-2-blue
[contributors-url]: https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/graphs/contributors
[forks-shield]: https://img.shields.io/badge/forks-0-brightgreen
[forks-url]: https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/network/members
[stars-shield]: https://img.shields.io/badge/stars-0-yellow
[stars-url]: https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/stargazers
[issues-shield]: https://img.shields.io/badge/issues-0%20open-brightgreen
[issues-url]: https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/issues
[license-shield]: https://img.shields.io/badge/license-AGPL-blue
[license-url]: https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/blob/master/LICENSE
