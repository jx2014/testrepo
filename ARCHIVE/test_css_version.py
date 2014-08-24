from file_construct import css_version_file

package_hr = '0200'
daily_folder = '20140728'
#css_version_path = r'C:\Users\ChilleeChillee\git\git\textfile.txt'
css_version_path = r'E:\FamilyProject\TestProject\GUI\textfile.txt'

cvfc = css_version_file(
                        package_hr = package_hr,
                        daily_folder = daily_folder,
                        css_version_path = css_version_path,
                        )

# cvfc.read_write_file()
# cvfc.change_date_from_css_version()
# cvfc.read_write_file('shit','dick')
cvfc.final_wrtie_new_date_css_version()