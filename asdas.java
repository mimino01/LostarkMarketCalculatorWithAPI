import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.json.JSONArray;
import org.json.JSONObject;

public class LostArkAPI {
    private static final String TOKEN = "YOUR_LOST_ARK_API_TOKEN";  // Token을 실제 API 토큰으로 대체
    private static final String URL = "https://developer-lostark.game.onstove.com/markets/items";

    private static HttpClient client = HttpClient.newHttpClient();

    public static List<Object> fetchItems(Map<String, Object> jsonData) {
        try {
            // JSON 데이터 생성
            JSONObject jsonObject = new JSONObject(jsonData);

            // 요청 생성
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(URL))
                    .header("accept", "application/json")
                    .header("authorization", TOKEN)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonObject.toString()))
                    .build();

            // 응답 처리
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            // 상태 코드 확인
            if (response.statusCode() != 200) {
                List<Object> errorResponse = new ArrayList<>();
                errorResponse.add(-1);
                errorResponse.add("요청 오류 발생: " + response.statusCode());
                return errorResponse;
            }

            // JSON 응답 파싱
            JSONObject responseBody = new JSONObject(response.body());
            JSONArray items = responseBody.optJSONArray("Items");
            return items != null ? items.toList() : new ArrayList<>();  // 'Items'가 없을 경우 빈 리스트 반환

        } catch (Exception e) {
            List<Object> errorResponse = new ArrayList<>();
            errorResponse.add(-1);
            errorResponse.add("오류 발생: " + e.getMessage());
            return errorResponse;
        }
    }

    public static List<Object> item() {
        List<Object> items = new ArrayList<>();
        int[] categoryCode = {90200, 90300, 90400, 90500, 90600, 90700};

        for (int code : categoryCode) {
            Map<String, Object> jsonData = new HashMap<>();
            jsonData.put("Sort", "GRADE");
            jsonData.put("CategoryCode", code);
            jsonData.put("SortCondition", "ASC");

            List<Object> result = fetchItems(jsonData);
            if ((int) result.get(0) == -1) {  // 오류 코드 확인
                return result;
            }
            items.add(result);
        }

        Map<String, Object> additionalData = new HashMap<>();
        additionalData.put("Sort", "GRADE");
        additionalData.put("CategoryCode", 50010);
        additionalData.put("ItemName", "융화");
        additionalData.put("SortCondition", "ASC");

        List<Object> additionalResult = fetchItems(additionalData);
        if ((int) additionalResult.get(0) == -1) {
            return additionalResult;
        }
        items.add(additionalResult);

        return items;
    }

    public static void main(String[] args) {
        List<Object> items = item();
        System.out.println(items);
    }
}
