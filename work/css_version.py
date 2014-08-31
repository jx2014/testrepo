from file_construct import css_version_file
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(r'C:\Users\ChilleeChillee\git\testrepo\work\path_config.ini')

#package_date = config.get('DailyPatch', 'package_date')
daily_folder = config.get('DailyPatch', 'Daily_folder')
package_hr = config.get('DailyPatch', 'package_hr')
#irci = config.get('DailyPatch', 'irci')

css_2400_version_file_path = config.get('css_versions','css_2400')
css_2401_version_file_path = config.get('css_versions','css_2401')
css_2401_csi2plus_version_file_path = config.get('css_versions','css_2401_csi2plus')
css_2500_version_file_path = config.get('css_versions','css_2500')


# cv2400 = css_version_file(csvp = css_2400_version_file_path)
# cv2401 = css_version_file(csvp = css_2401_version_file_path)
# cv2401_csi2plus = css_version_file(csvp = css_2401_csi2plus_version_file_path)
# cv2500 = css_version_file(csvp = css_2500_version_file_path)

#------------------

# package_hr = '0200'
# daily_folder = '20140728'
##css_version_path = r'C:\Users\ChilleeChillee\git\git\textfile.txt'
# css_version_path = r'E:\FamilyProject\TestProject\GUI\textfile.txt'

cv2400 = css_version_file(
                        package_hr = package_hr,
                        daily_folder = daily_folder,
                        css_version_path = css_2400_version_file_path,
                        )

cv2401 = css_version_file(
                        package_hr = package_hr,
                        daily_folder = daily_folder,
                        css_version_path = css_2401_version_file_path,
                        )

cv2401_csi2plus = css_version_file(
                        package_hr = package_hr,
                        daily_folder = daily_folder,
                        css_version_path = css_2401_csi2plus_version_file_path,
                        )

cv2500 = css_version_file(
                        package_hr = package_hr,
                        daily_folder = daily_folder,
                        css_version_path = css_2500_version_file_path,
                        )

cv2400.final_wrtie_new_date_css_version()
cv2401.final_wrtie_new_date_css_version()
cv2401_csi2plus.final_wrtie_new_date_css_version()
cv2500.final_wrtie_new_date_css_version()