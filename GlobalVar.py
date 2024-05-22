# 导入 tkinter 库，用于创建图形用户界面
import tkinter as tk

# 定义一个全局变量 userid，用于存储用户 ID，默认值为 1
userid = 1

# 创建一个 tkinter 窗口对象，后续会在这个窗口上添加各种界面元素
BigWindow = tk.Tk()

# 下面是各种数据文件的路径，这些文件将用于电影推荐系统
# movies.csv 包含电影的相关信息
pathmovie = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/movies.csv"

# links.csv 包含电影的外部链接
pathlink = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/links.csv"

# ratings.csv 包含用户对电影的评分数据
pathrating = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/ratings.csv"

# cosSim_ALS.pickle 包含基于 ALS 算法计算得到的电影相似度矩阵
pathcosSim_svd = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/cosSim_ALS.pickle"

# movie_similar_svd.csv 包含基于 SVD 算法计算得到的电影相似度矩阵
pathmovie_similar_svd = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/movie_similar_svd.csv"

# offline_recommend_svd.csv 包含基于 SVD 算法计算得到的离线推荐结果
pathoffline_recommend_svd = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/offline_recommend_svd.csv"

# offline_recommend_als.csv 包含基于 ALS 算法计算得到的离线推荐结果
pathoffline_recommend_als = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/offline_recommend_als.csv"

# movie_similar_als.csv 包含基于 ALS 算法计算得到的电影相似度矩阵
pathmovie_similar_als = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/movie_similar_als.csv"

# pathusers 包含用户数据
pathusers = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/users.csv"

# pathonline_recommend 包含根据用户的评分、喜好等信息为他们生成的在线推荐电影列表
pathonline_recommend = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/online_recommend.csv"

# pathmovieidlist 一个包含所有电影ID的序列化列表，用于在程序中快速查找和访问电影ID
pathmovieidlist = r"C:/Users/13729/Documents/WeChat Files/wxid_a6l9v8idcwc822/FileStorage/File/2023-04/create-movie_recommendation_system-from-0/MovieRecommendationSystem/data/movieidlist.pickle"



