import sys
from fastapi.testclient import TestClient

try:
    from app.main import app
    client = TestClient(app)
except Exception as e:
    print(f"FAILED TO IMPORT APP: {e}")
    sys.exit(1)

def run_feature3_tests():
    print("==================================================")
    print("RUNNING FEATURE 3: ADMIN SMART ALERTS & PRIORITY-BASED MONITORING TESTS")
    print("==================================================")

    # 1. Health check
    res = client.get("/api/health")
    assert res.status_code == 200, "Health check failed"
    print("[PASS] 1. GET /api/health returned 200 OK")

    # 2. Filter options includes Feature 3 options
    res = client.get("/api/admin/crop-monitoring/filters")
    assert res.status_code == 200
    filters = res.json()
    assert "health_statuses" in filters
    assert "verification_statuses" in filters
    assert "disease_statuses" in filters
    assert "priority_levels" in filters
    assert "Health Data Unavailable" in filters["health_statuses"]
    assert "Verification Required" in filters["verification_statuses"]
    assert "Rejected" in filters["verification_statuses"]
    print("[PASS] 2. Filter metadata returned verified options: health, disease, priority, verification.")

    # 3. Smart Alerts endpoint
    res = client.get("/api/admin/crop-monitoring/alerts?district=Tenkasi")
    assert res.status_code == 200
    alert_data = res.json()
    alerts = alert_data["alerts"]
    print(f"[PASS] 3. GET /api/admin/crop-monitoring/alerts:")
    print(f"         Pending Verification: {alerts['pending_verification']}")
    print(f"         Critical Crops (<50%): {alerts['critical_crops']}")
    print(f"         Disease / Pest Detected: {alerts['disease_detected']}")
    print(f"         High Priority: {alerts['high_priority']}")
    print(f"         Moderate Health: {alerts['moderate_health']}")
    print(f"         Healthy: {alerts['healthy_crops']}")
    assert alerts["high_priority"] > 0, "Expected non-zero high priority parcels"

    # 4. Multi-filter testing: Priority HIGH + Disease Detected
    res = client.get("/api/admin/crop-monitoring/markers?priority=HIGH&disease=Disease Detected&limit=50")
    assert res.status_code == 200
    m_data = res.json()
    print(f"[PASS] 4. Multi-filter test (Priority=HIGH & Disease=Disease Detected): matches = {m_data['total_matches']}")
    for m in m_data["markers"][:5]:
        assert m["priority"] == "HIGH", "Record must be classified as HIGH priority"
        assert m["disease_status"] == "Disease Detected", "Disease status mismatch"
        assert m["marker_color"] == "#991b1b", "Dark red color expected for active disease marker"
    print("         All markers returned correct status colors and priority tags.")

    # 5. Missing health data check
    res = client.get("/api/admin/crop-monitoring/records?health=Health Data Unavailable&page_size=5")
    assert res.status_code == 200
    unavail_records = res.json()
    print(f"[PASS] 5. Health Data Unavailable filter: {unavail_records['total_count']} records without telemetry.")
    if unavail_records["records"]:
        rec = unavail_records["records"][0]
        assert rec["health_score"] is None, "Missing health score must not default to any number"
        assert rec["health_status"] == "Health Data Unavailable"
        assert rec["priority"] in ["HIGH", "MEDIUM"], "Missing health cannot be LOW priority"

    # 6. Admin Action: Verify Record
    res = client.get("/api/admin/crop-monitoring/records?verification=Verification Required&page_size=1")
    assert res.status_code == 200
    recs = res.json().get("records", [])
    if recs:
        target_id = recs[0]["id"]
        update_res = client.put(f"/api/admin/crop-monitoring/records/{target_id}", json={
            "action": "VERIFY_RECORD",
            "verification_status": "Verified",
            "reason": "Field survey officer verified on-site"
        })
        assert update_res.status_code == 200
        updated = update_res.json()["record"]
        assert updated["verification_status"] == "Verified"
        print(f"[PASS] 6. Admin Action: Record {target_id} verified successfully.")

    # 7. Admin Action: Reject Record with Reason
    if len(recs) > 0:
        target_id = recs[0]["id"]
        update_res = client.put(f"/api/admin/crop-monitoring/records/{target_id}", json={
            "action": "REJECT_RECORD",
            "verification_status": "Rejected",
            "reason": "Field inspection confirmed land is currently fallow; incorrect crop declared."
        })
        assert update_res.status_code == 200
        rejected = update_res.json()["record"]
        assert rejected["verification_status"] == "Rejected"
        print(f"[PASS] 7. Admin Action: Record {target_id} rejected with mandatory reason.")

    # 8. Check Audit Log
    res = client.get("/api/admin/crop-monitoring/audit-log?limit=5")
    assert res.status_code == 200
    logs = res.json().get("audit_log", [])
    assert len(logs) > 0, "Audit log must contain recorded admin actions"
    latest_log = logs[0]
    print(f"[PASS] 8. Audit log verified: Action '{latest_log.get('action')}' recorded with reason '{latest_log.get('reason')}'")

    # 9. Non-regression check on Feature 1 and Feature 2
    res_rec = client.get("/api/crop-recommendations?survey_number=1342")
    assert res_rec.status_code == 200, "Crop recommendations regression"
    res_parcel = client.get("/api/parcels/1342")
    assert res_parcel.status_code == 200, "Farmer parcel regression"
    print("[PASS] 9. Non-regression: Feature 1 & Feature 2 endpoints operating cleanly.")

    print("\n==================================================")
    print("ALL FEATURE 3 VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_feature3_tests()
