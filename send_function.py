# from send_f2 import send_function
import glob
import csv
import os
import time
import logging
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from exception_handling import click_element_with_retry, find_element_with_retry
from open_whatapp import open_whatsapp_in_chrome
from other_functions import extract_numerical_digits, get_valid_input, file_exists, get_last_row_index

file_path = []


def file_exists_without_extension(base_name, directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        return False

    for file_name in os.listdir(directory):
        # Split the file name into base name and extension
        name, ext = os.path.splitext(file_name)
        # Check if the base name matches
        if name == base_name:
            return True
    return False


def read_unsent_contacts(file_path):
    unsent_contacts = []
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                unsent_contacts.append(row)
    return unsent_contacts


pass


def save_unsent_contacts(file_path, headers, unsent_contacts):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(unsent_contacts)


# Global variable to track whether open_chrom has been called and store the driver
chrom_opened = False
whatsapp_opened = False
driver = None


def open_chrom():
    global chrom_opened, driver
    if not chrom_opened:
        driver, chosen_port = open_whatsapp_in_chrome()
        if not driver:
            print("Failed to open WhatsApp. Exiting.")
            return False
        chrom_opened = True
    return True


def send_function(config, retry=False):
    print("enterd in send function")
    global whatsapp_opened
    if not open_chrom():
        return

    if not whatsapp_opened and not retry:
        input("Scan the QR code and press any key to continue")
        whatsapp_opened = True

    csv_file_path = os.path.abspath(config['csv_file_path'])
    start_row = config['start_row']
    end_row = config['end_row']
    file_sending_strategy = config['file_sending_strategy']
    file_folder_path = os.path.abspath(config.get('file_folder_path'))
    single_or_multiple_files = config.get('single_or_multiple_files')
    print(single_or_multiple_files)
    file_paths = os.path.abspath(config.get('file_paths'))
    file_extension = config.get('file_extension')
    message_sending_strategy = config['message_sending_strategy']
    template_message = config.get('template_message')
    math_column_index = config.get('math_column_index')
    science_column_index = config.get('science_column_index')
    hindi_column_index = config.get('hindi_column_index')
    english_column_index = config.get('english_column_index')
    social_science_column_index = config.get('social_science_column_index')
    message = config.get('message')
    contactname = config['contactname']
    contactnumber = config['contactnumber']
    unsent_contacts = []


    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)

            for i, row in enumerate(reader, 1):
                if i < start_row:
                    continue
                if i > end_row:
                    break

                contact_name = row[int(contactname)]
                raw_contact_number = row[int(contactnumber)]
                print(raw_contact_number)

                contact_number = extract_numerical_digits(raw_contact_number)
                print("1")

                if not contact_number:
                    logging.warning(f"Skipping contact {contact_name} because the contact number is empty.")
                    unsent_contacts.append(row)
                    continue
                print("2")
                if not contact_number.startswith("+91"):
                    contact_number = "+91" + contact_number
                print("3")
                if file_sending_strategy == 'different':
                    print("4")
                    file_path_pattern = os.path.join(file_folder_path, f"{contact_name}")
                    print("5")
                    file_path = file_path_pattern
                    print(file_path)
                    # Extract directory and base name
                    directory = os.path.dirname(file_path)
                    base_name = os.path.basename(file_path)

                else:
                    print("11")
                    if single_or_multiple_files == 'single':
                        print("12")
                        file_path = file_paths[0]
                        print("13")
                    else:
                        print("14")
                        file_path = file_paths[i % len(file_paths)]
                        print("15")

                if not os.path.exists(file_path):
                    print("16")
                    logging.error(f"No file found for {contact_name}. Skipping to the next contact.")
                    print("17")
                    unsent_contacts.append(row)
                    print("18")
                    continue


                print("19")
                new_chat_button_xpath = "//div[@title='New chat']//span[1]"
                print("20")
                try:
                    print("21")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, new_chat_button_xpath)))
                    print("22")
                    new_chat_button = find_element_with_retry(driver, By.XPATH, new_chat_button_xpath)
                    print("22")
                    if new_chat_button:
                        print("23")
                        click_element_with_retry(new_chat_button)
                        print("24")
                    else:
                        logging.error(f"Failed to open chat for {contact_name}. Skipping to the next contact.")
                        unsent_contacts.append(row)
                        continue
                except Exception as e:
                    logging.error(
                        f"Error opening chat for {contact_name}: {str(e)}. Skipping to the next contact.")
                    unsent_contacts.append(row)
                    continue

                time.sleep(0.2)

                chat_box = find_element_with_retry(driver, By.XPATH, "(//div[@contenteditable='true'])[1]")
                print("25")
                if chat_box:
                    chat_box.click()
                    chat_box.send_keys(contact_number)
                    time.sleep(0.3)
                    chat_box.send_keys(Keys.ENTER)
                else:
                    driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)
                    logging.error(f"Chat box not found for {contact_name}. Skipping to the next contact.")
                    unsent_contacts.append(row)
                    continue

                time.sleep(0.3)

                try:
                    print("26")
                    attachment_section = find_element_with_retry(driver, By.XPATH, "//div[@title='Attach']")
                    if attachment_section:
                        click_element_with_retry(attachment_section)
                    else:
                        print("27")
                        driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)
                        logging.error(
                            f"Failed to open attachment menu for {contact_name}. Skipping to the next contact.")
                        unsent_contacts.append(row)
                        continue
                except Exception as e:
                    logging.error(
                        f"Error opening attachment menu for {contact_name}: {str(e)}. Skipping to the next contact.")
                    unsent_contacts.append(row)
                    continue

                    # if file_extension.lower() in ['jpg', 'png', 'mp4', '3gpp', 'quicktime']:
                    # print("28")

                    xpath = "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
                    # else:
                    print("29")
                    # xpath = "(//li[@data-animate-dropdown-item='true']//div)[1]"

                file_box = find_element_with_retry(driver, By.XPATH,
                                                   "(//li[@data-animate-dropdown-item='true'])[2]")
                print("30")

                def find_element_with_retry1(driver, by, value, retries=3, delay=1):
                    for _ in range(retries):
                        try:
                            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
                            return element
                        except StaleElementReferenceException:
                            time.sleep(delay)
                    return None

                if file_box:
                    print(f"single_or_multiple_files: {single_or_multiple_files}")
                    print(f"file_paths: {file_paths}")
                    if single_or_multiple_files == 'multiple':
                        print("Entered multiple files block")
                        for path in file_paths:
                            try:
                                # Locate the file box again to avoid stale element reference
                                file_box = find_element_with_retry1(driver, By.XPATH, "//input[@type='file']")
                                if not file_box:
                                    logging.error(
                                        f"File box not found for {contact_name}. Skipping to the next contact.")
                                    unsent_contacts.append(row)
                                    continue

                                file_box.send_keys(path)
                                print(f"Processing file: {path}")

                                # Locate the send button again to avoid stale element reference
                                send_button_xpath = "//span[@data-icon='send']"
                                send_button = find_element_with_retry1(driver, By.XPATH, send_button_xpath)
                                if send_button:
                                    send_button.click()
                                    print("File sent")
                                    logging.info(f"File sent to {contact_name}")
                                else:
                                    logging.error(
                                        f"Failed to send file to {contact_name}. Skipping to the next contact.")
                                    unsent_contacts.append(row)
                                    continue

                                time.sleep(7)
                            except (NoSuchElementException, StaleElementReferenceException) as e:
                                logging.error(
                                    f"Error sending file to {contact_name}: {str(e)}. Skipping to the next contact.")
                                unsent_contacts.append(row)
                                continue
                    elif single_or_multiple_files == "single":
                        print("Entered single file block")
                        try:
                            # Locate the file box again to avoid stale element reference
                            file_box = find_element_with_retry(driver, By.XPATH, "//input[@type='file']")
                            if not file_box:
                                logging.error(f"File box not found for {contact_name}. Skipping to the next contact.")
                                unsent_contacts.append(row)
                                continue

                            file_box.send_keys(file_path)

                            # Locate the send button again to avoid stale element reference
                            send_button_xpath = "//span[@data-icon='send']"
                            send_button = find_element_with_retry(driver, By.XPATH, send_button_xpath)
                            if send_button:
                                send_button.click()
                                print("File sent")
                                logging.info(f"File sent to {contact_name}")
                            else:
                                logging.error(f"Failed to send file to {contact_name}. Skipping to the next contact.")
                                unsent_contacts.append(row)
                                continue

                            time.sleep(0.7)
                        except (NoSuchElementException, StaleElementReferenceException) as e:
                            logging.error(
                                f"Error sending file to {contact_name}: {str(e)}. Skipping to the next contact.")
                            unsent_contacts.append(row)
                            continue
                    else:
                        print("Entered different file block")
                        try:
                            # Locate the file box again to avoid stale element reference
                            file_box = find_element_with_retry(driver, By.XPATH, "//input[@type='file']")
                            if not file_box:
                                logging.error(f"File box not found for {contact_name}. Skipping to the next contact.")
                                unsent_contacts.append(row)
                                continue

                            file_box.send_keys(file_path)
                            print(file_path_pattern)

                            # Locate the send button again to avoid stale element reference
                            send_button_xpath = "//span[@data-icon='send']"
                            send_button = find_element_with_retry(driver, By.XPATH, send_button_xpath)
                            if send_button:
                                send_button.click()
                                print("File sent")
                                logging.info(f"File sent to {contact_name}")
                            else:
                                logging.error(f"Failed to send file to {contact_name}. Skipping to the next contact.")
                                unsent_contacts.append(row)
                                continue

                            time.sleep(0.7)
                        except (NoSuchElementException, StaleElementReferenceException) as e:
                            logging.error(
                                f"Error sending file to {contact_name}: {str(e)}. Skipping to the next contact.")
                            unsent_contacts.append(row)
                            continue
                else:
                    logging.error(f"File box not found for {contact_name}. Skipping to the next contact.")
                    unsent_contacts.append(row)
                    continue

                if message_sending_strategy == "different":
                    print("33")
                    math_marks = row[math_column_index]
                    science_marks = row[science_column_index]
                    hindi_marks = row[hindi_column_index]
                    english_marks = row[english_column_index]
                    social_science_marks = row[social_science_column_index]

                    message = template_message.replace("%placeholder1", str(math_marks))
                    message = message.replace("%placeholder2", str(science_marks))
                    message = message.replace("%placeholder3", str(hindi_marks))
                    message = message.replace("%placeholder4", str(english_marks))
                    message = message.replace("%placeholder5", str(social_science_marks))

                if message:
                    try:
                        print("34")
                        message_box = find_element_with_retry(driver, By.XPATH, "(//div[@contenteditable='true'])[2]")
                        if message_box:
                            message_box.click()
                            message_box.send_keys(message)
                            time.sleep(1.5)  # Adjust the timing as necessary
                            message_box.send_keys(Keys.ENTER)
                            driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)
                        else:
                            driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)
                            logging.error(f"Message box not found for {contact_name}. Skipping to the next contact.")
                            continue
                    except Exception as e:
                        logging.error(
                            f"Error sending message to {contact_name}: {str(e)}. Skipping to the next contact.")
                        continue

                time.sleep(0.2)
                print("escapekey")
                driver.find_element(By.XPATH, "//body").send_keys(Keys.ESCAPE)

                # Break for a few seconds after sending 20 images

                if i != 0 and i % 20 == 0:
                    logging.info(f"Sent 20 images. Taking a 15-second break.")
                    time.sleep(random.uniform(1, 5))
                    print(f"Sent 20 images. Taking a 1 to 5-second break.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        unsent_contacts.append(row)

    return unsent_contacts


def main():
    csv_file_path = get_valid_input("Enter the path of the CSV file: ", file_exists)
    start_row = int(get_valid_input("Enter the starting row number: ", lambda x: x.isdigit() and int(x) > 0))
    end_row = int(get_valid_input(f"Enter the ending row number (max {get_last_row_index(csv_file_path)}): ",
                                  lambda x: x.isdigit() and int(x) >= start_row))
    contactname = get_valid_input("Enter the column number for contact names: ", lambda x: x.isdigit())
    contactnumber = get_valid_input("Enter the column number for contact numbers: ", lambda x: x.isdigit())

    file_sending_strategy = get_valid_input(
        "Do you want to send the same file to all contacts or different files to each contact? (same/different): ",
        lambda x: x in ["same", "different"])
    file_paths = []
    file_extension = None
    file_folder_path = None
    single_or_multiple_files = None
    if file_sending_strategy == "same":
        single_or_multiple_files = get_valid_input(
            "Do you want to send the same single file or multiple files? (single/multiple): ",
            lambda x: x in ["single", "multiple"])
        if single_or_multiple_files == "single":
            file_path = get_valid_input("Enter the path of the file to be sent: ", file_exists)
            file_paths.append(file_path)
        else:
            file_paths = []
            while True:
                file_path = get_valid_input("Enter the path of a file to be sent (or type 'done' to finish): ",
                                            lambda x: file_exists(x) or x.lower() == 'done')
                if file_path.lower() == 'done':
                    break
                file_paths.append(file_path)
                print(file_paths)
    else:
        file_folder_path = get_valid_input("Enter the path of the folder containing the files to be sent: ",
                                           os.path.isdir)

    message_sending_strategy = get_valid_input(
        "Do you want to send the same message to all contacts or different messages? (same/different): ",
        lambda x: x in ["same", "different"])
    template_message = None
    math_column_index = None
    science_column_index = None
    hindi_column_index = None
    english_column_index = None
    social_science_column_index = None
    message = None

    if message_sending_strategy == "different":
        template_message = input(
            "Enter the template message with placeholders (e.g., 'Math: %placeholder1, Science: %placeholder2'): ")
        math_column_index = int(get_valid_input("Enter the column number for math marks: ", lambda x: x.isdigit()))
        science_column_index = int(
            get_valid_input("Enter the column number for science marks: ", lambda x: x.isdigit()))
        hindi_column_index = int(get_valid_input("Enter the column number for hindi marks: ", lambda x: x.isdigit()))
        english_column_index = int(
            get_valid_input("Enter the column number for english marks: ", lambda x: x.isdigit()))
        social_science_column_index = int(
            get_valid_input("Enter the column number for social science marks: ", lambda x: x.isdigit()))
    else:
        message = input("Enter the message to be sent: ")

    config = {
        'csv_file_path': csv_file_path,
        'start_row': start_row,
        'end_row': end_row,
        'file_sending_strategy': file_sending_strategy,
        'file_extension': file_extension,
        'file_folder_path': file_folder_path,
        'single_or_multiple_files': single_or_multiple_files,
        'file_paths': file_paths,
        'message_sending_strategy': message_sending_strategy,
        'template_message': template_message,
        'math_column_index': math_column_index,
        'science_column_index': science_column_index,
        'hindi_column_index': hindi_column_index,
        'english_column_index': english_column_index,
        'social_science_column_index': social_science_column_index,
        'message': message,
        'contactname': contactname,
        'contactnumber': contactnumber
    }
    print("this is from app", single_or_multiple_files)
    for paths in file_paths:
        print(paths)
    unsent_contacts_file = 'unsent_contacts.csv'
    max_attempts = 5

    # Initial sending attempt
    unsent_contacts = send_function(config)
    print("37")
    # Save the first batch of unsent contacts
    if unsent_contacts:
        print("38")
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            print("39")
            headers = next(reader)
        save_unsent_contacts(unsent_contacts_file, headers, unsent_contacts)
        print("40")
        print("Unsent contacts have been saved to 'unsent_contacts.csv'.")

    attempts = 1
    while unsent_contacts and attempts < max_attempts:
        print(f"Retrying unsent contacts... Attempt {attempts + 1}")
        config['csv_file_path'] = unsent_contacts_file  # Use the unsent contacts file for the next attempt
        unsent_contacts = send_function(config)
        attempts += 1
        if unsent_contacts:
            save_unsent_contacts(unsent_contacts_file, headers, unsent_contacts)
        else:
            if os.path.exists(unsent_contacts_file):
                os.remove(unsent_contacts_file)  # Remove the file if all contacts are successfully sent
            print("All contacts have been successfully sent.")
            break

    if unsent_contacts:
        save_unsent_contacts(unsent_contacts_file, headers, unsent_contacts)
        print(f"Final list of unsent contacts saved to '{unsent_contacts_file}' after {max_attempts} attempts.")


if __name__ == "__main__":
    main()
