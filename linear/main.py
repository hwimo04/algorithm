import os
from flask import Flask, request, jsonify

app = Flask(__name__)

def linear_search_trace(arr, target):
    """
    선형 검색(Linear Search)을 수행하면서 각 단계의 상태를 기록합니다.
    - arr: 검색 대상 리스트 (정수/문자열)
    - target: 찾고자 하는 값
    """
    steps = []
    found = False
    found_index = -1

    for idx, value in enumerate(arr):
        # 현재 인덱스와 비교 값 일치 여부 확인
        is_match = (value == target)
        
        # 단계별 진행 상태 기록
        steps.append({
            "step": idx + 1,
            "currentIndex": idx,
            "currentValue": value,
            "isMatch": is_match,
            "message": f"인덱스 {idx} (값: {value}) 검사 -> " + ("일치! 타깃을 찾았습니다." if is_match else "불일치. 다음으로 이동합니다.")
        })

        if is_match:
            found = True
            found_index = idx
            break  # 타깃을 찾았으므로 탐색 중단

    # 전체 탐색 종료 후 결과 요약
    summary = {
        "found": found,
        "index": found_index,
        "totalSteps": len(steps),
        "timeComplexity": "O(N) (최선: O(1), 최악: O(N))",
        "spaceComplexity": "O(1)"
    }

    return {"steps": steps, "summary": summary}

@app.route("/", methods=["GET"])
def health_check():
    """헬스 체크 및 기본 엔드포인트"""
    return jsonify({"status": "healthy", "service": "Linear Search API"}), 200

@app.route("/search", methods=["POST"])
def search():
    """
    클라이언트(GAS)로부터 배열과 타깃 값을 받아 선형 검색 실행
    Request JSON: {"array": [10, 20, 30], "target": 20}
    """
    data = request.get_json(silent=True)
    if not data or "array" not in data or "target" not in data:
        return jsonify({
            "error": "잘못된 요청입니다. 'array' 리스트와 'target' 값을 JSON 형식으로 전달하세요."
        }), 400

    arr = data.get("array")
    target = data.get("target")

    if not isinstance(arr, list):
        return jsonify({"error": "'array' 필드는 반드시 리스트여야 합니다."}), 400

    # 선형 탐색 및 단계별 결과 생성
    result = linear_search_trace(arr, target)
    result["input"] = {"array": arr, "target": target}

    return jsonify(result), 200

if __name__ == "__main__":
    # 로컬 테스트용 실행 설정
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
