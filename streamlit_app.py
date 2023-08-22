import os
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

API_KEY = 'AIzaSyDi27OID7eh35pvpNFTX6Ui0tspGXl48mY'

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

video_id = 'jV7qK1kfD70'

def get_all_video_comments(video_id):
    comments = []
    next_page_token = None
    while True:
        try:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                order='relevance',
                textFormat='plainText',
                pageToken=next_page_token
            )
            response = request.execute()
            comments.extend(response['items'])
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        except googleapiclient.errors.HttpError as e:
            print(f'An error occurred: {e}')
            break
    return comments

def sort_comments_by_votes(comments):
    sorted_comments = sorted(comments, key=lambda x: x['snippet']['topLevelComment']['snippet']['likeCount'], reverse=True)
    return sorted_comments

all_comments = get_all_video_comments(video_id)
sorted_comments = sort_comments_by_votes(all_comments)

# Convert sorted_comments to a pandas DataFrame
comments_data = []
for comment in sorted_comments:
    snippet = comment['snippet']['topLevelComment']['snippet']
    comments_data.append({
        'Author': snippet['authorDisplayName'],
        'Comment': snippet['textDisplay'],
        'Likes': snippet['likeCount'],
    })

df = pd.DataFrame(comments_data)
df

