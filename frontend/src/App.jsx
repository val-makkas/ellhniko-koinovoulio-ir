import { useState } from "react";
import "./App.css";

const API_BASE_URL = 
  typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000'
    : 'http://backend:8000';

function App() {
  const [activeTab, setActiveTab] = useState("search");
  
  // ========== SEARCH TAB STATE ==========
  // Αποθηκεύει δεδομένα για τη λειτουργία αναζήτησης
  const [query, setQuery] = useState("");              
  const [party, setParty] = useState("");              
  const [member, setMember] = useState("");            
  const [results, setResults] = useState([]);          
  const [loading, setLoading] = useState(false);       
  const [searchPerformed, setSearchPerformed] = useState(false);

  // ========== TIMELINE TAB STATE ==========
  // Αποθηκεύει δεδομένα για τη χρονολογική ανάλυση θεμάτων
  const [timelineMember, setTimelineMember] = useState(""); 
  const [timelineParty, setTimelineParty] = useState("");
  const [timelineData, setTimelineData] = useState(null);
  const [timelineLoading, setTimelineLoading] = useState(false); 
  const [timelineType, setTimelineType] = useState("member");

  // ========== TOPIC DRIFT TAB STATE ==========
  // Αποθηκεύει δεδομένα για τη ανάλυση εξέλιξης θεμάτων
  const [driftStartYear, setDriftStartYear] = useState(2015);
  const [driftEndYear, setDriftEndYear] = useState(2020);
  const [driftParty, setDriftParty] = useState("");
  const [driftData, setDriftData] = useState(null);
  const [driftLoading, setDriftLoading] = useState(false);
  const [driftType, setDriftType] = useState("all");

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setSearchPerformed(true);
    try {
      console.log("Search request starting...");
      const res = await fetch(`${API_BASE_URL}/api/search/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, top_k: 5, party, member }),
      });
      console.log("Response status:", res.status);
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      console.log("Data received:", data);
      setResults(data.results || []);
    } catch (err) {
      console.error("Search error:", err);
      alert("Error: " + err.message);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleTimelineSearch = async () => {
    setTimelineLoading(true);
    try {
      let url;
      if (timelineType === "member") {
        if (!timelineMember.trim()) return;
        url = `${API_BASE_URL}/api/keywords/member-timeline?name=${encodeURIComponent(timelineMember)}&top_n=5`;
      } else {
        if (!timelineParty.trim()) return;
        url = `${API_BASE_URL}/api/keywords/party-timeline?party=${encodeURIComponent(timelineParty)}&top_n=5`;
      }
      const res = await fetch(url);
      const data = await res.json();
      setTimelineData(data);
    } catch (err) {
      setTimelineData(null);
    } finally {
      setTimelineLoading(false);
    }
  };

  const handleTopicDrift = async () => {
    setDriftLoading(true);
    try {
      let url;
      if (driftType === "all") {
        url = `${API_BASE_URL}/api/analysis/topic-drift?start_year=${driftStartYear}&end_year=${driftEndYear}&top_n=8`;
      } else {
        if (!driftParty.trim()) return;
        url = `${API_BASE_URL}/api/analysis/topic-drift-by-party?party=${encodeURIComponent(driftParty)}&start_year=${driftStartYear}&end_year=${driftEndYear}&top_n=8`;
      }
      const res = await fetch(url);
      const data = await res.json();
      setDriftData(data);
    } catch (err) {
      setDriftData(null);
    } finally {
      setDriftLoading(false);
    }
  };

  const resetSearch = () => {
    setQuery("");
    setParty("");
    setMember("");
    setResults([]);
    setSearchPerformed(false);
  };

  /**
   * Reset χρονολογικής ανάλυσης - καθαρίζει όλα τα πεδία
   */
  const resetTimeline = () => {
    setTimelineMember("");
    setTimelineParty("");
    setTimelineData(null);
    setTimelineType("member");
  };

  /**
   * Reset ανάλυσης εξέλιξης θεμάτων - επαναφέρει στις προεπιλεγμένες τιμές
   */
  const resetDrift = () => {
    setDriftStartYear(2015);
    setDriftEndYear(2020);
    setDriftParty("");
    setDriftData(null);
    setDriftType("all");
  };

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: "0 auto", background: "#1a1a1a", minHeight: "100vh", color: "#e0e0e0" }}>
      <h1 style={{ color: "#ffffff" }}>Greek Parliament Analysis</h1>

      {/* ========== TAB NAVIGATION ========== */}
      {/* Πλοήγηση ανάμεσα στα τρία κύρια tabs */}
      <div style={{ display: "flex", gap: 8, marginBottom: 32, background: "#2d2d2d", padding: 8, borderRadius: 12 }}>
        {/* Search Tab Button */}
        <button
          onClick={() => setActiveTab("search")}
          style={{
            padding: "12px 24px",
            border: "none",
            background: activeTab === "search" ? "#007bff" : "transparent",
            color: activeTab === "search" ? "white" : "#b0b0b0",
            cursor: "pointer",
            fontWeight: activeTab === "search" ? "bold" : "600",
            fontSize: 15,
            borderRadius: 8,
            transition: "all 0.2s ease",
            boxShadow: activeTab === "search" ? "0 2px 8px rgba(0,123,255,0.3)" : "none",
          }}
          onMouseEnter={(e) => {
            if (activeTab !== "search") {
              e.target.style.background = "#3d3d3d";
              e.target.style.color = "#ffffff";
            }
          }}
          onMouseLeave={(e) => {
            if (activeTab !== "search") {
              e.target.style.background = "transparent";
              e.target.style.color = "#b0b0b0";
            }
          }}
        >
          Search
        </button>

        {/* Timeline Tab Button */}
        <button
          onClick={() => setActiveTab("timeline")}
          style={{
            padding: "12px 24px",
            border: "none",
            background: activeTab === "timeline" ? "#007bff" : "transparent",
            color: activeTab === "timeline" ? "white" : "#b0b0b0",
            cursor: "pointer",
            fontWeight: activeTab === "timeline" ? "bold" : "600",
            fontSize: 15,
            borderRadius: 8,
            transition: "all 0.2s ease",
            boxShadow: activeTab === "timeline" ? "0 2px 8px rgba(0,123,255,0.3)" : "none",
          }}
          onMouseEnter={(e) => {
            if (activeTab !== "timeline") {
              e.target.style.background = "#3d3d3d";
              e.target.style.color = "#ffffff";
            }
          }}
          onMouseLeave={(e) => {
            if (activeTab !== "timeline") {
              e.target.style.background = "transparent";
              e.target.style.color = "#b0b0b0";
            }
          }}
        >
          Keywords Timeline
        </button>

        {/* Topic Drift Tab Button */}
        <button
          onClick={() => setActiveTab("drift")}
          style={{
            padding: "12px 24px",
            border: "none",
            background: activeTab === "drift" ? "#007bff" : "transparent",
            color: activeTab === "drift" ? "white" : "#b0b0b0",
            cursor: "pointer",
            fontWeight: activeTab === "drift" ? "bold" : "600",
            fontSize: 15,
            borderRadius: 8,
            transition: "all 0.2s ease",
            boxShadow: activeTab === "drift" ? "0 2px 8px rgba(0,123,255,0.3)" : "none",
          }}
          onMouseEnter={(e) => {
            if (activeTab !== "drift") {
              e.target.style.background = "#3d3d3d";
              e.target.style.color = "#ffffff";
            }
          }}
          onMouseLeave={(e) => {
            if (activeTab !== "drift") {
              e.target.style.background = "transparent";
              e.target.style.color = "#b0b0b0";
            }
          }}
        >
          Topic Drift
        </button>
      </div>

      {/* ========== SEARCH TAB CONTENT ========== */}
      {activeTab === "search" && (
        <div>
          <h2 style={{ color: "#ffffff" }}>Full-Text Search</h2>
          <p style={{ color: "#a0a0a0", marginBottom: 20 }}>Search through 1.28 million parliamentary speeches from 1989-2020. Filter by party or member.</p>
          
          {/* Φόρμα αναζήτησης με τρία πεδία input */}
          <div style={{ display: "grid", gap: 8, marginBottom: 16 }}>
            {/* Πεδίο αναζήτησης */}
            <input
              style={{ padding: 8, background: "#2d2d2d", color: "#e0e0e0", border: "1px solid #444", borderRadius: 4 }}
              placeholder="Search keyword..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            
            {/* Φίλτρο κόμματος */}
            <input
              style={{ padding: 8, background: "#2d2d2d", color: "#e0e0e0", border: "1px solid #444", borderRadius: 4 }}
              placeholder="Party (optional)"
              value={party}
              onChange={(e) => setParty(e.target.value)}
            />
            
            {/* Φίλτρο μέλους */}
            <input
              style={{ padding: 8, background: "#2d2d2d", color: "#e0e0e0", border: "1px solid #444", borderRadius: 4 }}
              placeholder="Member (optional)"
              value={member}
              onChange={(e) => setMember(e.target.value)}
            />
            
            {/* Κουμπιά Search και Reset */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
              <button onClick={handleSearch} disabled={loading}>
                {loading ? "Searching..." : "Search"}
              </button>
              <button 
                onClick={resetSearch}
                style={{
                  padding: 8,
                  background: "#6c757d",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  cursor: "pointer",
                  fontWeight: "500"
                }}
              >
                Reset
              </button>
            </div>
          </div>

          {/* Εμφάνιση αποτελεσμάτων ή μηνυμάτων κενής κατάστασης */}
          <div>
            {/* Μήνυμα όταν δεν έχει γίνει αναζήτηση */}
            {results.length === 0 && !loading && !searchPerformed && (
              <div style={{ padding: 40, textAlign: "center", color: "#888", background: "#252525", borderRadius: 8 }}>
                Enter a search term to find relevant speeches
              </div>
            )}
            
            {/* Μήνυμα όταν δεν βρέθηκαν αποτελέσματα */}
            {results.length === 0 && !loading && searchPerformed && (
              <div style={{ padding: 40, textAlign: "center", color: "#ff9800", background: "#252525", borderRadius: 8, border: "1px solid #ff9800" }}>
                <div style={{ fontSize: 18, fontWeight: "bold", marginBottom: 8 }}>No results found</div>
                <div style={{ color: "#a0a0a0" }}>Try different keywords or remove filters to see more results</div>
              </div>
            )}
            
            {/* Εμφάνιση αποτελεσμάτων αναζήτησης */}
            {results.map((r, idx) => (
              <div key={idx} style={{ marginBottom: 16, borderBottom: "1px solid #444", paddingBottom: 8 }}>
                {/* Μέλος και κόμμα */}
                <div style={{ color: "#e0e0e0" }}><strong>{r.member_name}</strong> — {r.political_party}</div>
                {/* Ημερομηνία ομιλίας */}
                <div style={{ color: "#a0a0a0" }}><em>{r.sitting_date}</em></div>
                {/* Απόσπασμα της ομιλίας */}
                <p style={{ color: "#c0c0c0" }}>{r.snippet}...</p>
                {/* Score αναζήτησης */}
                <small style={{ color: "#888" }}>Score: {r.score}</small>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ========== TIMELINE TAB CONTENT ========== */}
      {activeTab === "timeline" && (
        <div>
          <h2 style={{ color: "#ffffff" }}>Keywords Timeline Evolution</h2>
          <p style={{ color: "#a0a0a0", marginBottom: 20 }}>Track how key topics evolved over time for specific members or political parties.</p>
          
          {/* Φόρμα επιλογής και αναζήτησης */}
          <div style={{ 
            padding: 24, 
            borderRadius: 8, 
            marginBottom: 24,
            border: "1px solid #444",
            background: "#252525"
          }}>
            <div style={{ display: "grid", gap: 12, marginBottom: 16 }}>
              {/* Radio buttons για επιλογή τύπου αναζήτησης */}
              <div style={{ display: "flex", gap: 20, alignItems: "center", justifyContent: "center" }}>
                <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", color: "#e0e0e0" }}>
                  <input
                    type="radio"
                    checked={timelineType === "member"}
                    onChange={() => setTimelineType("member")}
                  />
                  <span>Search by Member</span>
                </label>
                <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer", color: "#e0e0e0" }}>
                  <input
                    type="radio"
                    checked={timelineType === "party"}
                    onChange={() => setTimelineType("party")}
                  />
                  <span>Search by Party</span>
                </label>
              </div>

              {/* Πεδίο input ανάλογα με τον τύπο */}
              {timelineType === "member" ? (
                <input
                  style={{ 
                    padding: 12, 
                    borderRadius: 6,
                    border: "1px solid #555",
                    fontSize: 14,
                    background: "#2d2d2d",
                    color: "#e0e0e0"
                  }}
                  placeholder="Member name..."
                  value={timelineMember}
                  onChange={(e) => setTimelineMember(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleTimelineSearch()}
                />
              ) : (
                <input
                  style={{ 
                    padding: 12, 
                    borderRadius: 6,
                    border: "1px solid #555",
                    fontSize: 14,
                    background: "#2d2d2d",
                    color: "#e0e0e0"
                  }}
                  placeholder="Party name..."
                  value={timelineParty}
                  onChange={(e) => setTimelineParty(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleTimelineSearch()}
                />
              )}

              {/* Κουμπιά αναζήτησης και reset */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
                <button 
                  onClick={handleTimelineSearch} 
                  disabled={timelineLoading}
                  style={{
                    padding: 12,
                    borderRadius: 6,
                    border: "none",
                    background: "#007bff",
                    color: "#fff",
                    cursor: "pointer",
                    fontWeight: "bold",
                    fontSize: 14,
                    transition: "background 0.2s"
                  }}
                >
                  {timelineLoading ? "Loading..." : "Load Timeline"}
                </button>
                <button 
                  onClick={resetTimeline}
                  style={{
                    padding: 12,
                    borderRadius: 6,
                    border: "none",
                    background: "#6c757d",
                    color: "#fff",
                    cursor: "pointer",
                    fontWeight: "bold",
                    fontSize: 14,
                    transition: "background 0.2s"
                  }}
                >
                  Reset
                </button>
              </div>
            </div>
          </div>

          {/* Μήνυμα κενής κατάστασης */}
          {!timelineData && !timelineLoading && (
            <div style={{ padding: 40, textAlign: "center", color: "#888", background: "#252525", borderRadius: 8 }}>
              Select a search type and enter a name to view keyword evolution over time
            </div>
          )}

          {/* Εμφάνιση χρονολογικών δεδομένων */}
          {timelineData && (
            <div style={{ marginTop: 32 }}>
              <h3 style={{ marginBottom: 32, textAlign: "left", color: "#ffffff" }}>{timelineData.member || timelineData.party}</h3>
              {/* Grid layout με κάρτες για κάθε έτος */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 20 }}>
                {timelineData.timeline && timelineData.timeline.map((yearData, idx) => (
                  <div 
                    key={idx} 
                    style={{ 
                      padding: 20, 
                      background: "#2d2d2d",
                      border: "1px solid #444",
                      borderRadius: 8,
                      boxShadow: "0 2px 4px rgba(0,0,0,0.3)",
                      transition: "transform 0.2s, box-shadow 0.2s, border-color 0.2s",
                      cursor: "pointer"
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = "translateY(-2px)";
                      e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,123,255,0.4)";
                      e.currentTarget.style.borderColor = "#007bff";
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = "translateY(0)";
                      e.currentTarget.style.boxShadow = "0 2px 4px rgba(0,0,0,0.3)";
                      e.currentTarget.style.borderColor = "#444";
                    }}
                  >
                    {/* Ετικέτα έτους */}
                    <div style={{ color: "#ffffff", fontSize: 16, fontWeight: "bold", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                      {yearData.year}
                    </div>
                    {/* Κορυφαίες λέξεις-κλειδιά του έτους ως tags */}
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                      {yearData.keywords && yearData.keywords.map((keyword, kIdx) => (
                        <span
                          key={kIdx}
                          style={{
                            padding: "5px 12px",
                            background: "#007bff",
                            color: "#fff",
                            borderRadius: 16,
                            fontSize: 12,
                            fontWeight: "500"
                          }}
                        >
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ========== TOPIC DRIFT TAB CONTENT ========== */}
      {activeTab === "drift" && (
        <div>
          <h2 style={{ color: "#ffffff" }}>Topic Drift Analysis</h2>
          <p style={{ color: "#a0a0a0", marginBottom: 20 }}>Analyze how parliamentary discussion topics changed over specific time periods.</p>
          
          {/* Φόρμα ανάλυσης εξέλιξης θεμάτων */}
          <div style={{ display: "grid", gap: 8, marginBottom: 16 }}>
            {/* Radio buttons για επιλογή τύπου ανάλυσης */}
            <div>
              <label style={{ color: "#e0e0e0" }}>
                <input
                  type="radio"
                  checked={driftType === "all"}
                  onChange={() => setDriftType("all")}
                />
                All Parliament
              </label>
              <label style={{ marginLeft: 16, color: "#e0e0e0" }}>
                <input
                  type="radio"
                  checked={driftType === "party"}
                  onChange={() => setDriftType("party")}
                />
                By Party
              </label>
            </div>

            {/* Πεδίο κόμματος (εμφανίζεται μόνο αν επιλεγεί "By Party") */}
            {driftType === "party" && (
              <input
                style={{ padding: 8, background: "#2d2d2d", color: "#e0e0e0", border: "1px solid #444", borderRadius: 4 }}
                placeholder="Party name..."
                value={driftParty}
                onChange={(e) => setDriftParty(e.target.value)}
              />
            )}

            {/* Επιλογή ετών (αρχικό και τελικό) */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
              <div>
                <label style={{ color: "#e0e0e0" }}>Start Year:</label>
                <input
                  type="number"
                  min="1989"
                  max="2020"
                  value={driftStartYear}
                  onChange={(e) => setDriftStartYear(parseInt(e.target.value))}
                  style={{ width: "100%", padding: 8, background: "#2d2d2d", color: "#e0e0e0", border: "1px solid #444", borderRadius: 4 }}
                />
              </div>
              <div>
                <label style={{ color: "#e0e0e0" }}>End Year:</label>
                <input
                  type="number"
                  min="1989"
                  max="2020"
                  value={driftEndYear}
                  onChange={(e) => setDriftEndYear(parseInt(e.target.value))}
                  style={{ width: "100%", padding: 8, background: "#2d2d2d", color: "#e0e0e0", border: "1px solid #444", borderRadius: 4 }}
                />
              </div>
            </div>

            {/* Κουμπιά ανάλυσης και reset */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
              <button onClick={handleTopicDrift} disabled={driftLoading}>
                {driftLoading ? "Analyzing..." : "Analyze Topic Drift"}
              </button>
              <button 
                onClick={resetDrift}
                style={{
                  padding: 8,
                  background: "#6c757d",
                  color: "white",
                  border: "none",
                  borderRadius: 4,
                  cursor: "pointer",
                  fontWeight: "500"
                }}
              >
                Reset
              </button>
            </div>
          </div>

          {/* Μήνυμα κενής κατάστασης */}
          {!driftData && !driftLoading && (
            <div style={{ padding: 40, textAlign: "center", color: "#888", background: "#252525", borderRadius: 8 }}>
              Select analysis type and year range, then click Analyze to see topic evolution
            </div>
          )}

          {/* Εμφάνιση δεδομένων εξέλιξης θεμάτων */}
          {driftData && (
            <div>
              <h3 style={{ color: "#ffffff" }}>{driftData.party ? `${driftData.party} (${driftData.period})` : `Parliament (${driftData.period})`}</h3>
              {/* Εμφάνιση θεμάτων ανά έτος */}
              {driftData.timeline && driftData.timeline.map((yearData, idx) => (
                <div key={idx} style={{ marginBottom: 16, padding: 12, background: "#2d2d2d", borderRadius: 4, border: "1px solid #444" }}>
                  <h4 style={{ color: "#ffffff" }}>{yearData.year}</h4>
                  {/* Θέματα ως green tags */}
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {yearData.topics && yearData.topics.map((topic, tIdx) => (
                      <span
                        key={tIdx}
                        style={{
                          padding: "6px 14px",
                          background: "#28a745",
                          color: "white",
                          borderRadius: 16,
                          fontSize: 12,
                          fontWeight: "bold",
                        }}
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;