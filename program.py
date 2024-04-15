import pandas as pd 
import selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import multiprocessing  as mp




link = []

if os.path.exists('links.csv') == False:
	driver = webdriver.Chrome()
	for page in range(1,8):
		time.sleep(2)
		
		driver.get(f'https://shop.adidas.jp/item/?gender=mens&category=wear&order=1&page={page}')
		height = driver.execute_script('return window.innerHeight')
		for scroll in range(1,5):
			driver.execute_script(f"window.scrollBy(0,{height*1.6})")
			time.sleep(1)
		links = driver.find_elements(By.XPATH,"//div[@class='itemCardArea-cards test-card css-dhpxhu']/div/a")

		for i in links:
			link.append(i.get_attribute('href'))

	link = pd.DataFrame(link,columns=['Links'])
	link.to_csv('links.csv',index = False)

def crawling(link):
	
	driver = webdriver.Chrome()
	driver.maximize_window()
	
	for li in link:
		page1 = []
		page2 = []
		print(li) 
		driver.get(li)
		time.sleep(5)
		height = driver.execute_script('return window.innerHeight')

		breadcrumb = " / ".join(driver.find_element(By.XPATH,'//ul[@class="breadcrumbList clearfix test-breadcrumb css-2lfxqg"]').text.split('\n'))
		Category = driver.find_element(By.XPATH,"//a[@class='groupName']").text
		Product_name = driver.find_element(By.XPATH,"//h1[@class='itemTitle test-itemTitle']").text
		pricing = driver.find_element(By.XPATH,"//span[@class='price-value test-price-value']").text
		avail_size = None
		try:
			avail_size = ', '.join(driver.find_element(By.XPATH,"//ul[@class='sizeSelectorList']").text.split('\n'))
		except:
			avail_size = None
		sense_size = None
		try:
			sense_size = driver.find_element(By.XPATH,"//div[@class='bar']/span").get_attribute('class')[-3:].replace('_','.')
		except:
			sense_size = None
		# print(sense_size)
		
		img_li = []
		
		driver.execute_script(f"window.scrollBy(0,{height*1.5})")
		try:
			driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[3]/main/div/div/div[2]/div[1]/div/div/button').click()
			time.sleep(3)
		except:
			print(' ')


		imgs = driver.find_elements(By.XPATH,"//img[@class='test-img image test-image']")

		for im in imgs:
			img_li.append(im.get_attribute('src'))
   
		driver.execute_script(f"window.scrollBy(0,-450)")
		time.sleep(2)
		for scroll in range(5):
			try:
				button = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[1]/div[3]/main/div/div/div[2]/div[1]/div/div[1]/button')
				button.click()
				time.sleep(3)
				break
			except:
				driver.execute_script(f"window.scrollBy(0,65)")
				time.sleep(2)
		
		

		try:
			coordinated = driver.find_elements(By.XPATH,"//div[@class='coordinate_image']")
			for c in coordinated:
				action = ActionChains(driver)
				action.click(c).perform()
				time.sleep(2)

				c_product_name = driver.find_element(By.XPATH,"//span[@class='titleWrapper']").text
				c_product_pricing = driver.find_elements(By.XPATH,"//span[@class='price-value test-price-salePrice-value']")[0].text
				product_page_link = driver.find_element(By.XPATH,"//div[@class='image_wrapper']/a").get_attribute('href')
				print(product_page_link,c_product_pricing,c_product_name)

				product_number = str(product_page_link).split('/')[-1]
				c_image = driver.find_element(By.XPATH,"//img[@class='coordinate_item_image test-img']").get_attribute('src')
				page2.append([li,c_product_name,c_product_pricing,product_number,c_image,product_page_link])
		  
		except:
			print('')

		special = []
		# time.sleep(2)
		try:
			special_function = driver.find_elements(By.XPATH,"//div[@class='item_part details']")
			sp_img = driver.find_elements(By.XPATH,'//img[@class="illustrationBody"]')
			for sp in range(len(special_function)):
				txt = special_function[sp].text.split('\n')
				special = [sp_img[sp].get_attribute('src'),txt[0], txt[-1]]
		except:
			print(' ')


		title_description = ''
		general_description = ''
		item_description = ''
		try:
			title_description = driver.find_element(By.XPATH,"//h4[@class='heading itemFeature test-commentItem-subheading']").text
			general_description = driver.find_element(By.XPATH,"//div[@class='commentItem-mainText test-commentItem-mainText']").text
			item_description = driver.find_element(By.XPATH,"//ul[@class='articleFeatures description_part css-1lxspbu']").text

		except:
			title_description = ''
			general_description = ''
			item_description = ''

		height = driver.execute_script('return window.innerHeight')
		
		for scroll in range(1,5): 
				driver.execute_script(f"window.scrollBy(0,{height})")
				time.sleep(1)

		# time.sleep(1)
		page4 = pd.DataFrame()
		try:
			table_element = driver.find_element(By.XPATH,"//*[@class='sizeChart test-sizeChart css-l7ym9o']")
			rows = table_element.find_elements(By.TAG_NAME,"tr")
			rows = rows[len(rows)//2:]
			head = table_element.find_elements(By.TAG_NAME,"th")
			data = []
			for id,row in enumerate(rows):
				cells = row.find_elements(By.TAG_NAME,"td")
				row_data = [head[id].text]
				for cell in cells:
					row_data.append(cell.text)
				data.append(row_data)
			size_table = pd.DataFrame(data)
			size_table.columns = size_table.iloc[0]
			size_table = size_table[1:]
			size_table = size_table.to_string(index=False)
			dic = {
			'Product name':[li],
			'Table' : [size_table],
			}
			dic = pd.DataFrame(dic)
			page4 = pd.concat([page4, dic], ignore_index = True)
			page4.reset_index()
			page4.to_csv('table.csv',mode='a',index = False,header=False)
		except:
			print('')


		height = driver.execute_script('return window.innerHeight')
		driver.execute_script(f"window.scrollBy(0,{height+200})")
		time.sleep(3)

		rating = ''
		count_rating = ''
		positive_pct = ''

		try:
			rating = driver.find_element(By.XPATH,"//div[@class='BVRRRatingNormalOutOf']/span[1]").text
			count_rating = driver.find_element(By.XPATH,"//span[@class='BVRRNumber BVRRBuyAgainTotal']").text
			positive_pct = driver.find_element(By.XPATH,"//span[@class='BVRRBuyAgainPercentage']").text
		except:
			rating = ''
			count_rating = ''
			positive_pct = ''
			

		fit = None
		length = None
		quality = None
		Comfort  = None
		try:
			review1 = driver.find_elements(By.XPATH,"//div[@class='BVRRSecondaryRatingsContainer']/div/div[1]/div/div[2]/div[2]/img")
			try:
				fit = review1[0].get_attribute('title')
			except:
				fit = None
			try:
				length = review1[1].get_attribute('title')
			except:
				length = None
		except:
			fit = None
			length = None
		try:
			review2 = driver.find_elements(By.XPATH,"//div[@class='BVRRSecondaryRatingsContainer']/div/div[2]/div/div[2]/div[2]/img")
			try:
		
				quality = review2[0].get_attribute('title')
			except:
				quality = None
			try:	
				comfort = review2[1].get_attribute('title')
			except:
				comfort = None
		except:
			quality = None
			comfort = None


		driver.execute_script(f"window.scrollBy(0,{height*4})")
		time.sleep(2)

		s = ''
		try:
			tags = driver.find_elements(By.XPATH,"//div[@class='itemTagsPosition']/div/div/a")
			for tag in tags:
				s +=  tag.text +', '

			s = s[:-2]
		except:
			s = ''


		def check(path):
			try:
				driver.find_element(By.XPATH, path)
				return True
			except:
				return False

		page3 = []	
		try:
			for times in range(50):
				for ti in range(5):
					driver.execute_script(f"window.scrollBy(0,200)")
					bol = check('//*[@id="BVRRDisplayContentFooterID"]/div/a')
					review_title = driver.find_elements(By.XPATH,"//div[@class='BVRRReviewTitleContainer']/span[2]")
					if (bol == True) or (len(review_title) == int(count_rating)):
						break
					time.sleep(2)
				button = driver.find_element(By.XPATH,'//*[@id="BVRRDisplayContentFooterID"]/div/a')
				action = ActionChains(driver)
				action.click(button).perform()
				time.sleep(2)
			
			

		except:
			user_rating = driver.find_elements(By.XPATH,"//div[@id='BVRRRatingOverall_Review_Display']/div[2]/img")
			review_rating = driver.find_elements(By.XPATH,"//div[@id='BVRRRatingOverall_Review_Display']/div[2]/img")
			review_date = driver.find_elements(By.XPATH,"//div[@class='BVRRReviewDateContainer']/span[2]")
			review_title = driver.find_elements(By.XPATH,"//div[@class='BVRRReviewTitleContainer']/span[2]")
			review_description = driver.find_elements(By.XPATH,"//div[@class='BVRRReviewTextContainer']")
			review_id = driver.find_elements(By.XPATH,"//span[@class='BVRRValue BVRRUserNickname']")
			
			for revw in range(len(review_date)):
				page3.append([li,review_rating[revw].get_attribute('title'),review_date[revw].text,review_title[revw].text,review_description[revw].text,review_id[revw].text])

		
		

		try: 
			page1 = [li,breadcrumb,Category,Product_name,pricing,avail_size,sense_size,img_li,title_description,general_description,item_description,special,rating,count_rating,positive_pct,fit,length,quality,comfort,s]
			df1 = pd.DataFrame([page1], columns=['Product Link','Breadcrumb(Category)','Category','Product Name','Pricing','Available Size','Sense Size','Image URL','Description Title','Description','Description(Itemization)','Special Function','Rating','Number of Reviews','Recommendation Rate','Fitting Rating','Length Rating','Material Rating','Comfort Rating','KWs'])

			df1.to_csv('productData.csv',index=False,mode='a',header=False)
		except:
			pass
		try:
			df2 = pd.DataFrame(page2,columns=['Product Link','Coordinated Product Name','Coordinated Product Price','Coordinated Product Number','Coordinated Product Image Link','Coordinated Product Page URL'] )
			df2.to_csv('coordinateData.csv',mode='a',index=False,header=False)
		except:
			pass
		try:
			df3 = pd.DataFrame(page3,columns=['Product Link','Review Rating','Review Date','Review Title','Review Description','Review ID'])
			df3.to_csv('ratingData.csv',index=False,mode='a',header=False)
			page3 = []
		except:
			pass
		
		
 		
 
	driver.close()


link = pd.read_csv('links.csv')['Links'].values.tolist()
try:
	start = pd.read_csv('productData.csv')['Product Link'].dropna().values.tolist()
	
	link = [x for x in link if x not in start]
except:
	link


if __name__ == '__main__':
	cpu  =  4
	li = []
	x = len(link) //cpu
	for i in range(cpu):
		s = i*x
		e = s+x

		li.append(link[s:e])


	pool = mp.Pool(cpu)
	pool.map(crawling,li)
 
 
df1 = pd.read_csv('productData.csv')
df2 = pd.read_csv('coordinateData.csv')
df2 = df2.groupby('Product Link').apply(lambda x: x[['Coordinated Product Name','Coordinated Product Price','Coordinated Product Number','Coordinated Product Image Link','Coordinated Product Page URL']].reset_index(drop=True))

df3 =pd.read_csv('ratingData.csv')
df3 = df3.groupby('Product Link').apply(lambda x: x[['Review Rating','Review Date','Review Title','Review Description','Review ID']].reset_index(drop=True))

df4 = pd.read_csv('table.csv')


writer = pd.ExcelWriter('Adidas_info.xlsx', engine = 'xlsxwriter')
df1.to_excel(writer, sheet_name = 'productData',index=False )
df2.to_excel(writer, sheet_name = 'CoordinatedData')
df3.to_excel(writer, sheet_name = 'Reviews' )
df4.to_excel(writer, sheet_name = 'ProductSizeTable', index=False )
writer.close()