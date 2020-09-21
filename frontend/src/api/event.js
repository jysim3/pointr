import axios from 'axios';
import moment from 'moment';

export function getEvent(eventID) {
  return axios.get('/api/event', {
    params: {
      eventID
    }
  }).then(response => {
    const data = response.data.data;
    return {
      id: data.id,
      start: moment(data.start),
      end: moment(data.end),
      name: data.name,
      photo: data.photo,
      description: data.description,
      // preview: data.preview,
      location: data.location,
      // hasQR: data.hasQR,
      // 'hasAccessCode': self.hasAccessCode,
      // 'hasAdminSignin': self.hasAdminSignin,
      privacy: data.privacy,
      tags: data.tags,
      status: data.status,
      society: data.society,
      nAttendees: data.nAttendees
    }
  }).catch(error => {
    if (error.response) {
      if (error.response.data &&
          error.response.data.message &&
          error.response.data.message.eventID)
      {
        throw {
          "status": 404,
          "message": "Event not found"
        }
      }
    } else if (error.request) {
      // FIXME: backend will currently abort and respond with 500 if event code is invalid
      console.log(error.request);
      throw {
        "status": 404,
        "message": "Event not found"
      }
    } else {
      console.log('Error', error.message);
      throw {
        "status": 500,
        "message": "Sorry, seems like there is a bug in our site! Please contact us @ pointr.live/request and provide this code: '38904'"
      }
    }
  })
}
