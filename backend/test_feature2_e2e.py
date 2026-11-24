import sys
import json
from fastapi.testclient import TestClient

try:
    from app.main import app
    client = TestClient(app)
except Exception as e:
    print(f"FAILED TO IMPORT APP: {e}")
    sys.exit(1)

def run_tests():
    print("==================================================")
    print("RUNNING FEATURE 2 END-TO-END AUTOMATED VERIFICATION")
    print("==================================================")

    # 1. Test Health
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("[PASS] 1. GET /api/health returned 200 OK")

    # 2. Test Recommendation for Survey 1342
    res = client.get("/api/crop-recommendations?survey_number=1342&land_area=2.5")
    assert res.status_code == 200, f"Recommendations failed: {res.status_code}"
    data = res.json()
    assert "top_5_recommendations" in data, "Missing top_5_recommendations key"
    assert len(data["top_5_recommendations"]) == 5, f"Expected 5 recommendations, got {len(data['top_5_recommendations'])}"
    top_crop = data["top_5_recommendations"][0]
    print(f"[PASS] 2. GET /api/crop-recommendations: Top Crop = {top_crop['crop_name']} (Score: {top_crop['recommendation_score']})")
    total_net = top_crop['financials']['total_land']['total_net_profit']
    print(f"         Total Est. Net Profit for 2.5 acres: Rs. {total_net:,.2f}")
    assert top_crop["financials"]["total_land"]["land_area_acres"] == 2.5, "Acres scaling mismatch"
    assert top_crop["recommendation_score"] >= 80, "Expected top recommendation score >= 80"

    # 3. Test Profit Analysis Endpoint
    res = client.get("/api/crop-recommendations/1342/profit-analysis?crop_name=Rice (Paddy)&land_area=1.5")
    assert res.status_code == 200, f"Profit analysis failed: {res.status_code}"
    profit_data = res.json()
    assert "financials" in profit_data, "Missing financials in profit analysis"
    assert profit_data["financials"]["per_acre"]["gross_revenue"] > 0, "Gross revenue should be > 0"
    print(f"[PASS] 3. GET /api/crop-recommendations/1342/profit-analysis: Gross Rev = Rs. {profit_data['financials']['per_acre']['gross_revenue']:,.2f}, Net Profit = Rs. {profit_data['financials']['per_acre']['net_profit']:,.2f}")

    # 4. Test Market Trends Endpoint
    res = client.get("/api/crop-recommendations/1342/market-trends?crop=Rice (Paddy)")
    assert res.status_code == 200, f"Market trends failed: {res.status_code}"
    trends_data = res.json()
    assert "monthly_data" in trends_data, "Missing monthly_data"
    assert len(trends_data["monthly_data"]) == 6, "Expected 6 months of historical data"
    print(f"[PASS] 4. GET /api/crop-recommendations/1342/market-trends: 6-month APMC Mandi trends retrieved successfully. Latest modal price = Rs. {trends_data['modal_price']}/q")

    # 5. Test Admin Recommendation Analytics Endpoint
    res = client.get("/api/admin/crop-recommendations/analytics?district=Tenkasi")
    assert res.status_code == 200, f"Admin analytics failed: {res.status_code}"
    admin_data = res.json()
    assert "most_recommended_crops" in admin_data, "Missing most_recommended_crops in admin analytics"
    assert len(admin_data["most_recommended_crops"]) >= 1, "Expected at least 1 top recommended crop"
    print(f"[PASS] 5. GET /api/admin/crop-recommendations/analytics: Evaluated {admin_data['total_farmers_evaluated']} parcels. Lead crop = {admin_data['most_recommended_crops'][0]['crop']}")

    # 6. Verify Non-Regression on Feature 1 & Farmer Endpoints
    res = client.get("/api/parcels/1342")
    assert res.status_code == 200, f"Parcel 1342 failed: {res.status_code}"
    res = client.get("/api/admin/crop-monitoring/overview")
    assert res.status_code == 200, f"Admin overview failed: {res.status_code}"
    print("[PASS] 6. Regression check: /api/parcels/1342 and /api/admin/crop-monitoring/overview returned 200 OK")

    print("\nALL FEATURE 2 AUTOMATED INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
