import http from 'k6/http';
import {check} from 'k6';
let options = {
      duration: '600s',
};
// SEE https://k6.io/docs/testing-guides/api-load-testing to use this script
// Installation:: https://k6.io/docs/getting-started/installation
const SLEEP_DURATION = 0.1;
export default function() {
      var url = 'https://pointr.live/api/auth/register';
       const id = (__VU +""+ __ITER).slice(-2);

      var payload = JSON.stringify({
            zID: "z50200" + id,
            firstName: "User",
            lastName: "One",
            password: "asdfjkl;",
            commencementYear: 2020,
            studentType: "international",
            degreeType: "undergraduate",
            isArc: true
            });
      var params = {
              headers: {
                        'Content-Type': 'application/json',
                      },
            };
      let res = http.post(url, payload, params);
    console.log(res.body)
        check(res, {
            'status was 200': r => r.status == 200,
        })
}
