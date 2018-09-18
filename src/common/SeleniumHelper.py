
# Author: Bruce.Zhu(Jialin)

import sys
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains


class SeleniumHelper(object):
    def __init__(self):
        self.driver = None

    def start(self, url):
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        # print(self.driver.title)

    def quit(self):
        self.driver.quit()

    def screen_shot(self, shot_path, info):
        print("%s\%s_%s.png" % (shot_path, info, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())))
        self.driver.get_screenshot_as_file(
            "%s/%s_%s.png" % (shot_path, info, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())))

    def switch_frame(self, frame_type):
        try:
            if frame_type == "default":
                self.driver.switch_to_default_content()
            elif frame_type == "rightFrame":
                self.driver.switch_to_frame("rightFrame")
            elif frame_type == "leftFrame":
                self.driver.switch_to_frame("leftFrame")
            else:
                print("No such frame {}".format(frame_type), 'red')
        # except NotImplementedError as e:
        except Exception as e:
            print("Error when switch frame {}: {}".format(frame_type, e))
            sys.exit()
        else:
            return True

    def find_element(self, ele_type, value, timeout=20):
        """
        Args:
            ele_type(str): element type
            timeout(int): max time at finding element
            value(str): element attribute value
        Returns:
            ele(WebElement): return object of found element
        """
        ele = None
        try:
            if ele_type == "id":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_id(value))
                ele = self.driver.find_element_by_id(value)
            elif ele_type == "name":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_name(value))
                ele = self.driver.find_element_by_name(value)
            elif ele_type == "class_name":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_class_name(value))
                ele = self.driver.find_element_by_class_name(value)
            elif ele_type == "link_text":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_link_text(value))
                ele = self.driver.find_element_by_link_text(value)
            elif ele_type == "partial_link_text":
                WebDriverWait(self.driver, timeout).until(
                    lambda driver: self.driver.find_element_by_partial_link_text(value))
                ele = self.driver.find_element_by_partial_link_text(value)
            elif ele_type == "tag_name":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_tag_name(value))
                ele = self.driver.find_element_by_tag_name(value)
            elif ele_type == "xpath":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_xpath(value))
                ele = self.driver.find_element_by_xpath(value)
            elif ele_type == "xpath_":
                WebDriverWait(self.driver, timeout).until(lambda driver: self.driver.find_element_by_xpath(value))
                ele = self.driver.find_element_by_xpath(value)
                ActionChains(self.driver).move_to_element(ele).click().perform()
            else:
                print("No such locate element way {}".format(ele_type))
        except NotImplementedError as e:
            print(e)
        except TimeoutError as e:
            print(e)
            # sys.exit()
            # else:
            # return ele
        finally:
            return ele

    @staticmethod
    def exec_ele(ele, action, value=None):
        if action == 'click':
            try:
                ele.click()
            except Exception as e:
                print(e)
                return False
        elif action == 'send_keys':
            try:
                ele.send_keys(value)
            except Exception as e:
                print(e)
                return False
        else:
            print('No such action {}'.format(action))
            return False
        return True


if __name__ == '__main__':
    browser = SeleniumHelper()
    browser.start('https://www.baidu.com')
