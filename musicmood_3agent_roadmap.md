1. Create services/spotify/spotify_client.py
2. Define SpotifyClient class
3. Initialize with client_id and client_secret from config
4. Add connection initialization on first use (lazy loading)
5. Add client methods stubs for common operations
6. Implement request logging for debugging
7. Test client can be instantiated without errors
8. Document SpotifyClient interface

**Expected Output**: 
- SpotifyClient class created
- Proper initialization with credentials
- Ready for authentication
- Interface documented

**Verification Checklist**:
- [ ] SpotifyClient class created
- [ ] Initializes with credentials from config
- [ ] No immediate API calls on init
- [ ] Client methods defined
- [ ] Logging configured

---

### Subtask 4.1.2: Implement Authentication (Client Credentials Flow)

**Objective**: Implement Spotify OAuth2 client credentials authentication

**Steps**:
1. Implement get_access_token() method using Spotify API
2. Use client credentials flow (no user login needed)
3. Make POST request to Spotify token endpoint
4. Parse response to extract access token and expiration
5. Cache token in memory with expiration timestamp
6. Implement automatic token refresh before expiry
7. Handle authentication errors gracefully (invalid credentials)
8. Test token obtained successfully
9. Verify token can be used for API calls
10. Test automatic refresh when token expires

**Expected Output**: 
- Access token obtained from Spotify
- Token cached with expiration
- Token refreshed automatically
- No authentication errors

**Verification Checklist**:
- [ ] Token obtained successfully
- [ ] Token format valid (Bearer token)
- [ ] Token expiration tracked
- [ ] Token refreshed before expiry
- [ ] Caching works correctly
- [ ] Invalid credentials handled

---

### Subtask 4.1.3: Test API Connection and Rate Limiting

**Objective**: Verify Spotify API connection and understand rate limits

**Steps**:
1. Make test API call (search for a popular track)
2. Check response includes rate limit headers
3. Extract rate limit information from headers
4. Document Spotify rate limits from response and docs
5. Implement rate limit awareness (log remaining requests)
6. Test multiple rapid requests to understand limits
7. Verify rate limiting headers present in all responses
8. Verify no 429 (too many requests) errors in normal usage
9. Implement backoff strategy if rate limited

**Expected Output**: 
- API connection works
- Rate limits understood and documented
- Headers captured correctly
- Rate limiting logged
- Backoff strategy in place

**Verification Checklist**:
- [ ] Test API call succeeds
- [ ] Rate limit headers present
- [ ] Rate limits documented
- [ ] Multiple requests work
- [ ] No 429 errors in normal use
- [ ] Backoff strategy implemented

---

### Subtask 4.1.4: Implement Error Handling for API Failures

**Objective**: Add robust error handling for API failures

**Steps**:
1. Add try-catch for network failures
2. Add handling for 400 errors (invalid request)
3. Add handling for 401 errors (authentication failure)
4. Add handling for 404 errors (resource not found)
5. Add handling for 429 errors (rate limit exceeded)
6. Add handling for 500-503 errors (server errors)
7. Implement retry logic for 5xx errors (max 3 retries)
8. Implement exponential backoff between retries
9. Log all errors with full context
10. Test with various error scenarios
11. Test retry logic works correctly

**Expected Output**: 
- Network errors handled
- API errors caught and categorized
- Retries work for transient failures
- Clear error logging
- Exponential backoff implemented

**Verification Checklist**:
- [ ] Connection errors handled
- [ ] 4xx errors caught
- [ ] 5xx errors trigger retries
- [ ] Backoff increases exponentially
- [ ] Errors logged clearly
- [ ] No unhandled exceptions

---

## TASK 4.2: Agent 2 Tools - Spotify Search

### Subtask 4.2.1: Create search_spotify_by_mood Tool

**Objective**: Build tool that searches Spotify based on mood data

**Steps**:
1. Create tools/spotify_tools.py file
2. Define search_spotify_by_mood function
3. Function accepts mood_data dictionary as input
4. Based on mood, generate appropriate search queries
5. Use SpotifyClient to search Spotify
6. Retrieve 50-100 candidate tracks
7. Extract track metadata (id, name, artist, album, image, uri)
8. Return list of track dictionaries
9. Wrap function as LangChain Tool with description
10. Add error handling for search failures

**Expected Output**: 
- search_spotify_by_mood tool created
- Generates search queries from mood
- Returns 50-100 tracks
- Wrapped as LangChain Tool
- Error handling in place

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts mood_data input
- [ ] Generates search queries
- [ ] Searches Spotify successfully
- [ ] Returns track list
- [ ] Track metadata complete
- [ ] Wrapped as LangChain Tool
- [ ] Error handling present

---

### Subtask 4.2.2: Implement Intelligent Query Generation

**Objective**: Generate effective Spotify search queries from mood

**Steps**:
1. Create mood-to-query mapping dictionary
2. For "happy" mood: queries = ["happy", "feel good", "upbeat"]
3. For "energetic" mood: queries = ["workout", "energy", "pump up"]
4. For "calm" mood: queries = ["chill", "relax", "ambient"]
5. For "focus" mood: queries = ["lo-fi", "study", "focus beats"]
6. For "sad" mood: queries = ["sad songs", "melancholic", "emotional"]
7. For "stressed" mood: queries = ["calming", "stress relief"]
8. Adjust queries based on energy level (high energy = add "upbeat")
9. Adjust queries based on context (gym = add "workout", work = add "focus")
10. Generate 3-5 diverse queries per mood
11. Test query generation for each mood type
12. Verify queries return relevant results

**Expected Output**: 
- Query generation logic implemented
- Covers all mood types
- Queries vary by energy/context
- Generates 3-5 queries per mood
- Queries return relevant results

**Verification Checklist**:
- [ ] Query mapping created
- [ ] All mood types covered
- [ ] Energy level affects queries
- [ ] Context affects queries
- [ ] 3-5 queries generated
- [ ] Queries return relevant tracks

---

### Subtask 4.2.3: Test Search with Various Moods

**Objective**: Verify search works for different mood types

**Steps**:
1. Test happy mood search
   - Verify returns upbeat, positive tracks
2. Test energetic mood search
   - Verify returns high-energy tracks
3. Test calm mood search
   - Verify returns relaxing tracks
4. Test focus mood search
   - Verify returns lo-fi, ambient tracks
5. Test sad mood search
   - Verify returns emotional tracks
6. For each mood, verify 50+ tracks returned
7. For each mood, verify track relevance
8. Test with high energy level (9-10)
   - Verify more intense tracks
9. Test with low energy level (1-3)
   - Verify calmer tracks
10. Document search quality for each mood

**Expected Output**: 
- All mood types return relevant tracks
- Track count adequate (50+)
- Track relevance high
- Energy level affects results
- Search quality documented

**Verification Checklist**:
- [ ] Happy mood search works
- [ ] Energetic mood search works
- [ ] Calm mood search works
- [ ] Focus mood search works
- [ ] Sad mood search works
- [ ] 50+ tracks per search
- [ ] Track relevance high
- [ ] Energy level affects results

---

### Subtask 4.2.4: Add Search Result Caching

**Objective**: Cache search results in Redis for performance

**Steps**:
1. Create cache key from mood data (hash of mood values)
2. Before searching, check Redis cache
3. If cache hit, return cached results
4. If cache miss, perform Spotify search
5. Store search results in Redis with TTL (1 hour)
6. Serialize track list as JSON for storage
7. Test cache hit scenario (second identical search)
8. Verify cache hit is significantly faster (<100ms)
9. Test cache expiration after TTL
10. Test cache with different mood combinations
11. Monitor cache hit rate

**Expected Output**: 
- Search results cached in Redis
- Cache hits return results quickly
- TTL set to 1 hour
- Cache hit rate tracked
- Significant performance improvement

**Verification Checklist**:
- [ ] Cache key generated from mood
- [ ] Cache checked before search
- [ ] Results stored in Redis
- [ ] TTL set to 1 hour
- [ ] Cache hit <100ms
- [ ] Cache miss performs search
- [ ] Cache expires correctly

---

## TASK 4.3: Agent 2 Tools - Audio Analysis

### Subtask 4.3.1: Create get_audio_features_batch Tool

**Objective**: Build tool to retrieve audio features for multiple tracks

**Steps**:
1. In tools/spotify_tools.py, define get_audio_features_batch function
2. Function accepts list of track IDs as input
3. Use Spotify API to get audio features (batch call, up to 100 tracks)
4. Extract audio features for each track:
   - energy (0-1)
   - danceability (0-1)
   - valence (positivity 0-1)
   - tempo (BPM)
   - acousticness (0-1)
   - instrumentalness (0-1)
   - liveness (0-1)
   - speechiness (0-1)
5. Return dictionary mapping track_id to features
6. Handle tracks with missing features
7. Wrap function as LangChain Tool
8. Add error handling for API failures

**Expected Output**: 
- get_audio_features_batch tool created
- Retrieves features for multiple tracks
- All 8 features extracted
- Missing features handled
- Wrapped as LangChain Tool

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts track ID list
- [ ] Batch API call implemented
- [ ] All 8 features extracted
- [ ] Features in correct ranges
- [ ] Missing features handled
- [ ] Returns feature dictionary
- [ ] Wrapped as LangChain Tool

---

### Subtask 4.3.2: Implement Batch Processing

**Objective**: Efficiently process audio features in batches

**Steps**:
1. Split large track lists into batches of 100 (Spotify limit)
2. Process each batch with single API call
3. Combine results from all batches
4. Implement parallel processing if beneficial
5. Add progress tracking for large batches
6. Test with 10 tracks (single batch)
7. Test with 150 tracks (2 batches)
8. Test with 500 tracks (5 batches)
9. Measure time per batch
10. Verify all tracks processed correctly

**Expected Output**: 
- Batch processing implemented
- Handles any number of tracks
- Efficient API usage
- Progress tracked
- All tracks processed

**Verification Checklist**:
- [ ] Batching logic implemented
- [ ] Max 100 tracks per batch
- [ ] Multiple batches handled
- [ ] Results combined correctly
- [ ] Works with 10 tracks
- [ ] Works with 150 tracks
- [ ] Works with 500 tracks
- [ ] Performance acceptable

---

### Subtask 4.3.3: Add Feature Caching

**Objective**: Cache audio features in Redis

**Steps**:
1. Create cache key for each track: "features:{track_id}"
2. Before API call, check cache for each track
3. Separate tracks into cached and uncached
4. Only fetch features for uncached tracks
5. Store fetched features in Redis with TTL (7 days)
6. Combine cached and fetched features
7. Test cache hit scenario (same tracks)
8. Verify cache reduces API calls
9. Test cache expiration
10. Monitor cache hit rate
11. Calculate API call reduction percentage

**Expected Output**: 
- Features cached in Redis
- Cache checked before API call
- TTL set to 7 days
- Significant API call reduction
- Cache hit rate tracked

**Verification Checklist**:
- [ ] Cache key format correct
- [ ] Cache checked for each track
- [ ] Only uncached tracks fetched
- [ ] Features stored in cache
- [ ] TTL set to 7 days
- [ ] Cache hit reduces API calls
- [ ] Cache expires correctly

---

## TASK 4.4: Agent 2 Tools - Track Filtering

### Subtask 4.4.1: Create filter_tracks_by_criteria Tool

**Objective**: Build tool to filter tracks based on mood requirements

**Steps**:
1. In tools/spotify_tools.py, define filter_tracks_by_criteria function
2. Function accepts tracks (with features) and mood_data as inputs
3. Based on mood, define filtering criteria:
   - For energetic: energy > 0.7, tempo > 120
   - For calm: energy < 0.5, tempo < 100
   - For focus: instrumentalness > 0.5
   - For happy: valence > 0.6
   - For sad: valence < 0.4
4. Filter tracks that don't meet criteria
5. Return filtered track list
6. Wrap function as LangChain Tool
7. Add logging for filtering decisions

**Expected Output**: 
- filter_tracks_by_criteria tool created
- Filtering logic for each mood type
- Inappropriate tracks removed
- Wrapped as LangChain Tool
- Filtering logged

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts tracks and mood_data
- [ ] Filtering criteria defined
- [ ] Energetic mood filters correctly
- [ ] Calm mood filters correctly
- [ ] Focus mood filters correctly
- [ ] Happy mood filters correctly
- [ ] Sad mood filters correctly
- [ ] Wrapped as LangChain Tool

---

### Subtask 4.4.2: Implement Filtering Logic

**Objective**: Implement robust filtering with multiple criteria

**Steps**:
1. For each mood, define multiple criteria
2. Combine criteria with AND logic (all must match)
3. Add tolerance ranges (e.g., energy 0.6-0.8 instead of exactly 0.7)
4. Adjust criteria based on energy_level from mood
5. Adjust criteria based on emotional_intensity
6. Handle edge cases (no tracks pass filters)
7. If too few tracks remain, relax criteria
8. Log how many tracks filtered out
9. Test filtering reduces track count appropriately
10. Test filtering improves track relevance

**Expected Output**: 
- Filtering logic implemented
- Multiple criteria per mood
- Tolerance ranges used
- Edge cases handled
- Filtering improves relevance

**Verification Checklist**:
- [ ] Multiple criteria per mood
- [ ] Criteria use tolerance ranges
- [ ] Energy level affects criteria
- [ ] Intensity affects criteria
- [ ] Edge cases handled
- [ ] Criteria relaxed if needed
- [ ] Filtering logged

---

### Subtask 4.4.3: Test Filtering Accuracy

**Objective**: Verify filtering improves track relevance

**Steps**:
1. Get 100 random tracks from Spotify
2. Filter for energetic mood
3. Manually verify filtered tracks are energetic
4. Calculate filtering accuracy (% correct)
5. Repeat for calm mood
6. Repeat for focus mood
7. Repeat for happy mood
8. Repeat for sad mood
9. Document accuracy for each mood type
10. Aim for >85% accuracy
11. Refine criteria if accuracy low

**Expected Output**: 
- Filtering accuracy measured
- >85% accuracy for each mood
- Inappropriate tracks removed
- Relevant tracks retained
- Accuracy documented

**Verification Checklist**:
- [ ] Energetic filtering >85% accurate
- [ ] Calm filtering >85% accurate
- [ ] Focus filtering >85% accurate
- [ ] Happy filtering >85% accurate
- [ ] Sad filtering >85% accurate
- [ ] Accuracy documented
- [ ] Criteria refined if needed

---

## TASK 4.5: Build Agent 2 with ReAct Pattern

### Subtask 4.5.1: Create Music Discovery Agent

**Objective**: Build Agent 2 using LangChain's ReAct pattern

**Steps**:
1. Create agents/discovery_agent.py file
2. Import create_react_agent from LangChain
3. Define agent prompt template for music discovery
4. Prompt should instruct agent to:
   - Use search_spotify_by_mood to find candidates
   - Use get_audio_features_batch to analyze tracks
   - Use filter_tracks_by_criteria to refine results
   - Think step-by-step (ReAct pattern)
   - Return filtered track list (50+ tracks)
5. Create list of tools for agent (3 tools)
6. Create agent using create_react_agent with Ollama LLM
7. Test agent can be instantiated

**Expected Output**: 
- Music Discovery Agent created
- Uses ReAct pattern
- Has access to 3 tools
- Prompt configured
- Agent instantiates successfully

**Verification Checklist**:
- [ ] Agent file created
- [ ] Agent uses ReAct pattern
- [ ] Prompt template defined
- [ ] 3 tools provided to agent
- [ ] Agent created successfully
- [ ] No instantiation errors

---

### Subtask 4.5.2: Configure Agent with 3 Tools

**Objective**: Properly configure agent with tools and executor

**Steps**:
1. Create AgentExecutor wrapping the agent
2. Pass 3 tools to executor
3. Configure max_iterations (set to 5 for discovery complexity)
4. Configure verbose mode for debugging
5. Enable handle_parsing_errors
6. Enable return_intermediate_steps
7. Set timeout for agent execution (60 seconds for API calls)
8. Test executor can be invoked
9. Verify executor returns track list

**Expected Output**: 
- AgentExecutor configured
- Max iterations set to 5
- Verbose logging enabled
- Error handling enabled
- Timeout configured
- Executor works

**Verification Checklist**:
- [ ] AgentExecutor created
- [ ] 3 tools provided
- [ ] max_iterations set to 5
- [ ] verbose=True
- [ ] handle_parsing_errors=True
- [ ] Timeout set to 60s
- [ ] Can invoke executor

---

### Subtask 4.5.3: Test Agent Search Strategy

**Objective**: Verify agent makes intelligent search decisions

**Steps**:
1. Invoke agent with happy mood data
2. Observe agent's reasoning (check logs)
3. Verify agent calls search_spotify_by_mood first
4. Verify agent then calls get_audio_features_batch
5. Verify agent finally calls filter_tracks_by_criteria
6. Check agent uses tools in logical order
7. Verify agent returns 50+ filtered tracks
8. Test with energetic mood
9. Verify agent adjusts search queries appropriately
10. Test agent handles API failures gracefully
11. Verify agent doesn't make redundant tool calls

**Expected Output**: 
- Agent follows logical search strategy
- Tools called in correct order
- Search queries appropriate for mood
- Returns adequate filtered tracks
- Handles failures gracefully

**Verification Checklist**:
- [ ] Agent calls search tool first
- [ ] Agent calls audio features tool second
- [ ] Agent calls filter tool third
- [ ] Tool order is logical
- [ ] Returns 50+ tracks
- [ ] Search queries appropriate
- [ ] Handles API failures
- [ ] No redundant calls

---

### Subtask 4.5.4: Add Agent Logging

**Objective**: Implement comprehensive logging for Agent 2

**Steps**:
1. Add structured logging to agent execution
2. Log when agent starts
3. Log each search query generated
4. Log number of tracks found
5. Log batch processing progress
6. Log filtering decisions
7. Log final track count
8. Log execution time
9. Log any errors or warnings
10. Verify logs capture all steps
11. Test logs are parseable and useful

**Expected Output**: 
- Comprehensive logging implemented
- All agent actions logged
- Execution time tracked
- Errors logged with context
- Logs useful for debugging

**Verification Checklist**:
- [ ] Agent execution logged
- [ ] Search queries logged
- [ ] Track counts logged
- [ ] Batch progress logged
- [ ] Filtering logged
- [ ] Execution time logged
- [ ] Errors logged
- [ ] Logs useful

---

## TASK 4.6: Agent 2 Integration Testing

### Subtask 4.6.1: Test End-to-End Discovery Process

**Objective**: Test complete Agent 2 workflow

**Steps**:
1. Provide Agent 2 with happy mood data
2. Verify agent searches Spotify
3. Verify agent retrieves audio features
4. Verify agent filters tracks
5. Verify final output has 50+ tracks
6. Verify all tracks have required metadata
7. Test with energetic mood data
8. Test with calm mood data
9. Test with focus mood data
10. Test with sad mood data
11. For each, verify appropriate tracks returned
12. Document success rate for each mood

**Expected Output**: 
- Complete workflow works for all moods
- 50+ tracks returned for each
- Tracks are relevant to mood
- All metadata present
- Success rate documented

**Verification Checklist**:
- [ ] Happy mood works end-to-end
- [ ] Energetic mood works
- [ ] Calm mood works
- [ ] Focus mood works
- [ ] Sad mood works
- [ ] 50+ tracks for each
- [ ] Tracks relevant
- [ ] Metadata complete

---

### Subtask 4.6.2: Test with Various Mood Types

**Objective**: Test Agent 2 with diverse mood inputs

**Steps**:
1. Test with high energy mood (energy=9)
   - Verify high-tempo, energetic tracks
2. Test with low energy mood (energy=2)
   - Verify calm, low-tempo tracks
3. Test with neutral mood (energy=5)
   - Verify balanced tracks
4. Test with work context
   - Verify focus/productivity tracks
5. Test with gym context
   - Verify workout tracks
6. Test with sleep context
   - Verify very calm, relaxing tracks
7. For each, verify track features match mood
8. Document track quality for each variant

**Expected Output**: 
- Agent adapts to energy levels
- Agent adapts to context
- Track features match requirements
- Quality consistent across variants
- Results documented

**Verification Checklist**:
- [ ] High energy tracks appropriate
- [ ] Low energy tracks appropriate
- [ ] Neutral energy tracks balanced
- [ ] Work context tracks appropriate
- [ ] Gym context tracks appropriate
- [ ] Sleep context tracks appropriate
- [ ] Track features match mood
- [ ] Quality consistent

---

### Subtask 4.6.3: Test Error Handling

**Objective**: Verify Agent 2 handles errors gracefully

**Steps**:
1. Test with Spotify API down (simulate)
   - Verify agent handles gracefully
   - Verify error logged clearly
2. Test with rate limiting (429 error)
   - Verify agent retries with backoff
   - Verify eventual success or clear failure
3. Test with invalid mood data
   - Verify agent handles or uses defaults
4. Test with network timeout
   - Verify timeout enforced
   - Verify partial results or clear error
5. Test with database cache failure
   - Verify agent falls back to API
6. For each error, verify agent doesn't crash
7. For each error, verify useful error messages

**Expected Output**: 
- All error scenarios handled
- No crashes
- Clear error messages
- Fallbacks work where possible
- Errors logged appropriately

**Verification Checklist**:
- [ ] API down handled
- [ ] Rate limiting handled
- [ ] Invalid mood handled
- [ ] Network timeout handled
- [ ] Cache failure handled
- [ ] No crashes
- [ ] Error messages clear

---

### Subtask 4.6.4: Benchmark Agent 2 Performance

**Objective**: Measure and document Agent 2 performance

**Steps**:
1. Run 10 test cases with various moods
2. Measure average execution time (target: 3-5 seconds)
3. Measure p95 latency
4. Measure p99 latency
5. Test with cache hit scenario
6. Measure cache hit latency (target: 1-2 seconds)
7. Count average API calls per execution
8. Measure cache hit rate percentage
9. Document all metrics in table
10. Identify performance bottlenecks if any
11. Verify performance meets requirements (< 5s avg)

**Expected Output**: 
- Performance metrics documented
- Average latency 3-5 seconds
- Cache hits 1-2 seconds
- p95 and p99 acceptable
- Cache hit rate high (>60%)
- Bottlenecks identified if any

**Verification Checklist**:
- [ ] Average latency measured (<5s)
- [ ] p95 latency acceptable
- [ ] p99 latency acceptable
- [ ] Cache hit latency <2s
- [ ] Cache hit rate >60%
- [ ] API calls counted
- [ ] Metrics documented
- [ ] Performance meets requirements

---

# PHASE 4 COMPLETION VERIFICATION

Before moving to Phase 5, verify all Phase 4 outputs:

**Spotify Client**:
- [ ] SpotifyClient class created
- [ ] Authentication implemented
- [ ] API connection tested
- [ ] Error handling in place
- [ ] Rate limiting understood

**Tool 3: Spotify Search**:
- [ ] search_spotify_by_mood tool created
- [ ] Intelligent query generation works
- [ ] Returns 50+ tracks
- [ ] Search results cached
- [ ] Wrapped as LangChain Tool

**Tool 4: Audio Features**:
- [ ] get_audio_features_batch tool created
- [ ] Batch processing implemented
- [ ] All 8 features extracted
- [ ] Features cached
- [ ] Wrapped as LangChain Tool

**Tool 5: Track Filtering**:
- [ ] filter_tracks_by_criteria tool created
- [ ] Filtering logic for all moods
- [ ] >85% filtering accuracy
- [ ] Wrapped as LangChain Tool

**Agent 2: Music Discovery**:
- [ ] Agent created with ReAct pattern
- [ ] Configured with 3 tools
- [ ] Search strategy logical
- [ ] Logging implemented

**Testing**:
- [ ] End-to-end workflow works
- [ ] All mood types handled
- [ ] Error scenarios handled
- [ ] Performance benchmarked
- [ ] Metrics within requirements

**Status**: Phase 4 ✅ COMPLETE - Ready for Phase 5

---

# PHASE 5: Multi-Agent System - Agent 3 (Playlist Curator) & Orchestration (Day 5)

## Phase 5 Overview
This phase implements the third agent (Playlist Curator) and connects all three agents in a sequential pipeline with proper orchestration.

### Phase 5 Tasks & Subtasks
```
PHASE 5
├── TASK 5.1: Agent 3 Tools - Track Ranking
│   ├── Subtask 5.1.1: Create rank_tracks_by_relevance tool
│   ├── Subtask 5.1.2: Implement ranking algorithm
│   └── Subtask 5.1.3: Test ranking quality
├── TASK 5.2: Agent 3 Tools - Diversity Optimization
│   ├── Subtask 5.2.1: Create optimize_diversity tool
│   ├── Subtask 5.2.2: Implement diversity logic
│   └── Subtask 5.2.3: Test diversity metrics
├── TASK 5.3: Agent 3 Tools - Explanation Generation
│   ├── Subtask 5.3.1: Create generate_explanation tool
│   ├── Subtask 5.3.2: Implement explanation templates
│   └── Subtask 5.3.3: Test explanation quality
├── TASK 5.4: Build Agent 3 with ReAct Pattern
│   ├── Subtask 5.4.1: Create Playlist Curator Agent
│   ├── Subtask 5.4.2: Configure agent with 3 tools
│   ├── Subtask 5.4.3: Test agent curation strategy
│   └── Subtask 5.4.4: Add agent logging
├── TASK 5.5: Multi-Agent Orchestration
│   ├── Subtask 5.5.1: Create orchestrator function
│   ├── Subtask 5.5.2: Connect Agent 1 → Agent 2 → Agent 3
│   ├── Subtask 5.5.3: Implement data flow between agents
│   └── Subtask 5.5.4: Add orchestration logging
└── TASK 5.6: End-to-End Integration Testing
    ├── Subtask 5.6.1: Test complete 3-agent pipeline
    ├── Subtask 5.6.2: Test with various user inputs
    ├── Subtask 5.6.3: Test error propagation
    └── Subtask 5.6.4: Benchmark complete system performance
```

---

## TASK 5.1: Agent 3 Tools - Track Ranking

### Subtask 5.1.1: Create rank_tracks_by_relevance Tool

**Objective**: Build tool to rank tracks by mood relevance

**Steps**:
1. Create tools/curator_tools.py file
2. Define rank_tracks_by_relevance function
3. Function accepts tracks (with features), mood_data, and user_context
4. Calculate relevance score for each track (0-100)
5. Score based on:
   - Audio feature match to mood (40% weight)
   - User preference alignment (30% weight)
   - Track popularity (20% weight)
   - Novelty/diversity (10% weight)
6. Sort tracks by score descending
7. Return ranked track list with scores
8. Wrap function as LangChain Tool
9. Add logging for ranking decisions

**Expected Output**: 
- rank_tracks_by_relevance tool created
- Scoring algorithm implemented
- Tracks ranked by score
- Wrapped as LangChain Tool
- Ranking logged

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts tracks, mood, context
- [ ] Calculates relevance score
- [ ] Audio features weighted 40%
- [ ] User preferences weighted 30%
- [ ] Popularity weighted 20%
- [ ] Diversity weighted 10%
- [ ] Tracks sorted by score
- [ ] Wrapped as LangChain Tool

---

### Subtask 5.1.2: Implement Ranking Algorithm

**Objective**: Implement detailed ranking logic

**Steps**:
1. For audio feature matching:
   - Compare track features to mood requirements
   - Calculate distance/similarity score
   - Normalize to 0-100 range
2. For user preference matching:
   - Check if track artist in user's favorites
   - Check if track genre matches user's preferences
   - Give bonus for past positive feedback
3. For popularity:
   - Use Spotify popularity metric (0-100)
   - Balance popular with niche tracks
4. For novelty:
   - Penalize tracks too similar to recent listens
   - Reward tracks from new artists
5. Combine scores with weighted sum
6. Handle missing data gracefully (use defaults)
7. Test ranking with sample tracks
8. Verify higher scored tracks are more relevant

**Expected Output**: 
- Ranking algorithm complete
- All components weighted correctly
- Missing data handled
- Higher scores = more relevant
- Algorithm tested

**Verification Checklist**:
- [ ] Audio feature matching implemented
- [ ] User preference matching implemented
- [ ] Popularity component implemented
- [ ] Novelty component implemented
- [ ] Weighted sum calculated correctly
- [ ] Missing data handled
- [ ] Scores normalized to 0-100
- [ ] Higher scores more relevant

---

### Subtask 5.1.3: Test Ranking Quality

**Objective**: Verify ranking improves playlist quality

**Steps**:
1. Create test set of 100 tracks
2. Rank for happy mood
3. Manually verify top 10 tracks are relevant
4. Check bottom 10 tracks are less relevant
5. Calculate ranking quality metric
6. Repeat for energetic mood
7. Repeat for calm mood
8. Repeat for focus mood
9. Document ranking quality for each mood
10. Aim for >80% top-10 relevance
11. Refine algorithm if quality low

**Expected Output**: 
- Ranking quality measured
- >80% top-10 relevance
- Top tracks clearly better than bottom
- Quality documented for all moods
- Algorithm refined if needed

**Verification Checklist**:
- [ ] Happy mood ranking >80% relevant
- [ ] Energetic mood ranking >80% relevant
- [ ] Calm mood ranking >80% relevant
- [ ] Focus mood ranking >80% relevant
- [ ] Top 10 significantly better than bottom 10
- [ ] Quality documented
- [ ] Algorithm refined if needed

---

## TASK 5.2: Agent 3 Tools - Diversity Optimization

### Subtask 5.2.1: Create optimize_diversity Tool

**Objective**: Build tool to ensure playlist diversity

**Steps**:
1. In tools/curator_tools.py, define optimize_diversity function
2. Function accepts ranked tracks and desired count (default 30)
3. Implement diversity constraints:
   - Maximum 2 songs per artist
   - Tempo variety (spread across tempo range)
   - Genre variety if genre data available
   - Energy curve (mix of high/medium/low energy)
4. Select top N tracks while respecting constraints
5. Reorder tracks for good flow (energy curve)
6. Return optimized playlist
7. Wrap function as LangChain Tool
8. Add logging for diversity decisions

**Expected Output**: 
- optimize_diversity tool created
- Diversity constraints implemented
- Returns N tracks with good variety
- Flow optimization included
- Wrapped as LangChain Tool

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts ranked tracks and count
- [ ] Artist constraint (max 2 per artist)
- [ ] Tempo variety ensured
- [ ] Energy curve optimized
- [ ] Returns requested count
- [ ] Tracks reordered for flow
- [ ] Wrapped as LangChain Tool

---

### Subtask 5.2.2: Implement Diversity Logic

**Objective**: Implement detailed diversity optimization

**Steps**:
1. Create artist counter to track songs per artist
2. As selecting tracks, check artist count
3. Skip track if artist already has 2 songs
4. Track tempo distribution across selected tracks
5. Prefer tracks that fill gaps in tempo distribution
6. Calculate energy curve: gradual changes preferred over sudden jumps
7. Reorder tracks to create smooth energy progression
8. Handle case where constraints prevent reaching desired count
9. Relax constraints if needed to reach count
10. Test diversity optimization with various inputs
11. Verify constraints are respected

**Expected Output**: 
- Diversity logic implemented
- Artist constraint enforced
- Tempo distribution spread
- Energy curve smooth
- Constraints respected
- Desired count achieved

**Verification Checklist**:
- [ ] Artist counting implemented
- [ ] Max 2 per artist enforced
- [ ] Tempo distribution tracked
- [ ] Gaps in tempo filled
- [ ] Energy curve calculated
- [ ] Tracks reordered smoothly
- [ ] Constraints relaxed if needed
- [ ] Desired count achieved

---

### Subtask 5.2.3: Test Diversity Metrics

**Objective**: Measure and verify diversity quality

**Steps**:
1. Generate playlist of 30 tracks
2. Count unique artists (should be 15+)
3. Calculate tempo standard deviation (should be >20 BPM)
4. Calculate energy standard deviation (should be >0.15)
5. Check for monotonous sections (5+ similar tracks in a row)
6. Calculate diversity score (0-100)
7. Test with various moods
8. Document diversity metrics for each
9. Aim for diversity score >70
10. Refine logic if diversity low

**Expected Output**: 
- Diversity metrics measured
- Unique artists 15+
- Tempo spread adequate
- Energy spread adequate
- No monotonous sections
- Diversity score >70

**Verification Checklist**:
- [ ] Unique artists counted (15+)
- [ ] Tempo spread measured (>20 BPM std dev)
- [ ] Energy spread measured (>0.15 std dev)
- [ ] No 5+ similar tracks in row
- [ ] Diversity score calculated
- [ ] Score >70 for all moods
- [ ] Metrics documented

---

## TASK 5.3: Agent 3 Tools - Explanation Generation

### Subtask 5.3.1: Create generate_explanation Tool

**Objective**: Build tool to explain playlist choices

**Steps**:
1. In tools/curator_tools.py, define generate_explanation function
2. Function accepts final playlist and original mood_data
3. Analyze playlist characteristics:
   - Average energy level
   - Average tempo
   - Most common genres
   - Artist diversity
4. Use Ollama LLM to generate natural language explanation
5. Explanation should include:
   - Why these tracks match the mood
   - Key characteristics of the playlist
   - How it addresses user's context
6. Keep explanation concise (2-3 sentences)
7. Return explanation string
8. Wrap function as LangChain Tool

**Expected Output**: 
- generate_explanation tool created
- Analyzes playlist characteristics
- Uses LLM for natural language
- Explanation concise and relevant
- Wrapped as LangChain Tool

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts playlist and mood
- [ ] Analyzes characteristics
- [ ] Uses Ollama LLM
- [ ] Explanation natural language
- [ ] Concise (2-3 sentences)
- [ ] Explains mood match
- [ ] Wrapped as LangChain Tool

---

### Subtask 5.3.2: Implement Explanation Templates

**Objective**: Create templates for consistent explanations

**Steps**:
1. Create explanation template for each mood type
2. Happy mood template: "upbeat tracks", "positive vibes", "feel-good"
3. Energetic mood template: "high-energy", "pump-up", "motivational"
4. Calm mood template: "relaxing", "soothing", "peaceful"
5. Focus mood template: "concentration", "productivity", "ambient"
6. Sad mood template: "emotional", "reflective", "cathartic"
7. Include playlist stats in template (tempo, energy)
8. Personalize with user context if available
9. Test templates generate appropriate explanations
10. Verify explanations are accurate and helpful

**Expected Output**: 
- Templates created for all moods
- Templates include mood-specific language
- Stats incorporated naturally
- Personalization included
- Explanations accurate

**Verification Checklist**:
- [ ] Happy mood template created
- [ ] Energetic mood template created
- [ ] Calm mood template created
- [ ] Focus mood template created
- [ ] Sad mood template created
- [ ] Stats included in templates
- [ ] Personalization added
- [ ] Explanations accurate

---

### Subtask 5.3.3: Test Explanation Quality

**Objective**: Verify explanations are helpful and accurate

**Steps**:
1. Generate playlists for 5 different moods
2. Generate explanations for each
3. Read each explanation
4. Verify explanation accurately describes playlist
5. Verify explanation mentions mood match
6. Verify explanation is helpful to user
7. Check for grammatical errors
8. Check for template artifacts (e.g., placeholder text)
9. Rate explanation quality (1-5 scale)
10. Document quality scores
11. Refine templates if quality low

**Expected Output**: 
- Explanations tested for all moods
- All explanations accurate
- All explanations helpful
- No grammatical errors
- Quality scores documented
- Average quality >4/5

**Verification Checklist**:
- [ ] 5 explanations generated
- [ ] All describe playlist accurately
- [ ] All mention mood match
- [ ] All helpful to users
- [ ] No grammatical errors
- [ ] No template artifacts
- [ ] Quality scores >4/5
- [ ] Templates refined if needed

---

## TASK 5.4: Build Agent 3 with ReAct Pattern

### Subtask 5.4.1: Create Playlist Curator Agent

**Objective**: Build Agent 3 using LangChain's ReAct pattern

**Steps**:
1. Create agents/curator_agent.py file
2. Import create_react_agent from LangChain
3. Define agent prompt template for playlist curation
4. Prompt should instruct agent to:
   - Use rank_tracks_by_relevance to score tracks
   - Use optimize_diversity to build final playlist
   - Use generate_explanation to explain choices
   - Think step-by-step (ReAct pattern)
   - Return final playlist with explanation
5. Create list of tools for agent (3 tools)
6. Create agent using create_react_agent with Ollama LLM
7. Test agent can be instantiated

**Expected Output**: 
- Playlist Curator Agent created
- Uses ReAct pattern
- Has access to 3 tools
- Prompt configured
- Agent instantiates successfully

**Verification Checklist**:
- [ ] Agent file created
- [ ] Agent uses ReAct pattern
- [ ] Prompt template defined
- [ ] 3 tools provided to agent
- [ ] Agent created successfully
- [ ] No instantiation errors

---

### Subtask 5.4.2: Configure Agent with 3 Tools

**Objective**: Properly configure agent with tools and executor

**Steps**:
1. Create AgentExecutor wrapping the agent
2. Pass 3 tools to executor
3. Configure max_iterations (set to 3 for curation)
4. Configure verbose mode for debugging
5. Enable handle_parsing_errors
6. Enable return_intermediate_steps
7. Set timeout for agent execution (30 seconds)
8. Test executor can be invoked
9. Verify executor returns playlist with explanation

**Expected Output**: 
- AgentExecutor configured
- Max iterations set to 3
- Verbose logging enabled
- Error handling enabled
- Timeout configured
- Executor works

**Verification Checklist**:
- [ ] AgentExecutor created
- [ ] 3 tools provided
- [ ] max_iterations set to 3
- [ ] verbose=True
- [ ] handle_parsing_errors=True
- [ ] Timeout set to 30s
- [ ] Can invoke executor

---

### Subtask 5.4.3: Test Agent Curation Strategy

**Objective**: Verify agent makes intelligent curation decisions

**Steps**:
1. Provide agent with 50 candidate tracks and mood data
2. Observe agent's reasoning (check logs)
3. Verify agent calls rank_tracks_by_relevance first
4. Verify agent then calls optimize_diversity
5. Verify agent finally calls generate_explanation
6. Check agent uses tools in logical order
7. Verify agent returns 30-track playlist
8. Verify playlist has good diversity
9. Verify explanation is present and accurate
10. Test agent handles edge cases (too few candidates)
11. Verify agent doesn't make redundant tool calls

**Expected Output**: 
- Agent follows logical curation strategy
- Tools called in correct order
- Returns 30-track playlist
- Diversity optimized
- Explanation generated
- Edge cases handled

**Verification Checklist**:
- [ ] Agent calls ranking tool first
- [ ] Agent calls diversity tool second
- [ ] Agent calls explanation tool third
- [ ] Tool order is logical
- [ ] Returns 30 tracks
- [ ] Diversity good
- [ ] Explanation present
- [ ] Edge cases handled

---

### Subtask 5.4.4: Add Agent Logging

**Objective**: Implement comprehensive logging for Agent 3

**Steps**:
1. Add structured logging to agent execution
2. Log when agent starts
3. Log ranking results (top 10 tracks by score)
4. Log diversity optimization decisions
5. Log final track selection
6. Log explanation generation
7. Log execution time
8. Log any errors or warnings
9. Verify logs capture all steps
10. Test logs are useful for debugging

**Expected Output**: 
- Comprehensive logging implemented
- All agent actions logged
- Execution time tracked
- Errors logged with context
- Logs useful for debugging

**Verification Checklist**:
- [ ] Agent execution logged
- [ ] Ranking results logged
- [ ] Diversity decisions logged
- [ ] Final selection logged
- [ ] Explanation logged
- [ ] Execution time logged
- [ ] Errors logged
- [ ] Logs useful

---

## TASK 5.5: Multi-Agent Orchestration

### Subtask 5.5.1: Create Orchestrator Function

**Objective**: Build main orchestration function for 3-agent pipeline

**Steps**:
1. Create services/orchestrator.py file
2. Define generate_playlist_with_agents function
3. Function accepts user_input (mood text) and user_id
4. Function will coordinate all 3 agents sequentially
5. Add error handling for entire pipeline
6. Add logging for orchestration
7. Add performance tracking (total time)
8. Return final playlist with metadata
9. Test orchestrator function can be called

**Expected Output**: 
- Orchestrator function created
- Accepts user input and user_id
- Coordinates agents
- Error handling in place
- Logging configured
- Function callable

**Verification Checklist**:
- [ ] Orchestrator file created
- [ ] Function defined
- [ ] Accepts user_input and user_id
- [ ] Error handling present
- [ ] Logging configured
- [ ] Performance tracking added
- [ ] Function callable

---

### Subtask 5.5.2: Connect Agent 1 → Agent 2 → Agent 3

**Objective**: Implement sequential agent execution

**Steps**:
1. In orchestrator, call Agent 1 (Mood Understanding) first
2. Pass user_input and user_id to Agent 1
3. Extract mood_data from Agent 1 output
4. Call Agent 2 (Music Discovery) with mood_data
5. Extract candidate_tracks from Agent 2 output
6. Call Agent 3 (Playlist Curator) with candidate_tracks and mood_data
7. Extract final_playlist and explanation from Agent 3 output
8. Return final result
9. Test complete pipeline executes
10. Verify each agent receives correct input

**Expected Output**: 
- Agents connected sequentially
- Data flows Agent 1 → Agent 2 → Agent 3
- Each agent receives correct input
- Final playlist returned
- Pipeline executes successfully

**Verification Checklist**:
- [ ] Agent 1 called first
- [ ] mood_data extracted
- [ ] Agent 2 called with mood_data
- [ ] candidate_tracks extracted
- [ ] Agent 3 called with tracks and mood
- [ ] final_playlist extracted
- [ ] Complete pipeline executes
- [ ] Correct data flow

---

### Subtask 5.5.3: Implement Data Flow Between Agents

**Objective**: Ensure proper data formatting between agents

**Steps**:
1. Define data structures for inter-agent communication
2. Agent 1 output format: mood_data dictionary
3. Agent 2 output format: list of track dictionaries
4. Agent 3 output format: final playlist + explanation
5. Add validation between stages
6. Ensure Agent 2 receives properly formatted mood_data
7. Ensure Agent 3 receives properly formatted tracks
8. Add data transformation if needed
9. Handle missing or invalid data gracefully
10. Test data flow with various inputs
11. Verify data integrity throughout pipeline

**Expected Output**: 
- Data structures defined
- Validation between stages
- Proper formatting ensured
- Missing data handled
- Data integrity maintained

**Verification Checklist**:
- [ ] Data structures defined
- [ ] Agent 1 output format validated
- [ ] Agent 2 receives proper mood_data
- [ ] Agent 2 output format validated
- [ ] Agent 3 receives proper tracks
- [ ] Agent 3 output format validated
- [ ] Missing data handled
- [ ] Data integrity verified

---

### Subtask 5.5.4: Add Orchestration Logging

**Objective**: Implement comprehensive pipeline logging

**Steps**:
1. Log orchestration start with user_input
2. Log Agent 1 start and completion time
3. Log mood_data summary
4. Log Agent 2 start and completion time
5. Log candidate track count
6. Log Agent 3 start and completion time
7. Log final playlist summary
8. Log total pipeline execution time
9. Log any errors at any stage
10. Create structured log format
11. Verify logs capture complete workflow

**Expected Output**: 
- Complete pipeline logged
- Each stage logged with timing
- Summaries at each stage
- Total execution time tracked
- Errors logged clearly

**Verification Checklist**:
- [ ] Pipeline start logged
- [ ] Agent 1 timing logged
- [ ] mood_data logged
- [ ] Agent 2 timing logged
- [ ] Track count logged
- [ ] Agent 3 timing logged
- [ ] Final playlist logged
- [ ] Total time logged
- [ ] Errors logged

---

## TASK 5.6: End-to-End Integration Testing

### Subtask 5.6.1: Test Complete 3-Agent Pipeline

**Objective**: Test full system from user input to final playlist

**Steps**:
1. Test case 1: "I'm feeling happy and energetic"
   - Verify Agent 1 extracts happy/energetic mood
   - Verify Agent 2 finds appropriate tracks
   - Verify Agent 3 creates 30-track playlist
   - Verify explanation matches mood
2. Test case 2: "Need to focus on work"
   - Verify focus mood extracted
   - Verify lo-fi/ambient tracks found
   - Verify playlist aids concentration
3. Test case 3: "Late night relaxation"
   - Verify calm mood extracted
   - Verify relaxing tracks found
   - Verify smooth energy curve
4. For each test, verify complete workflow
5. For each test, measure total execution time
6. Document results for all test cases

**Expected Output**: 
- All test cases pass
- Complete workflow functions
- Execution time acceptable
- Final playlists appropriate
- Results documented

**Verification Checklist**:
- [ ] Happy/energetic test passes
- [ ] Focus test passes
- [ ] Relaxation test passes
- [ ] All workflows complete
- [ ] Execution time <10s
- [ ] Playlists appropriate
- [ ] Results documented

---

### Subtask 5.6.2: Test with Various User Inputs

**Objective**: Test system with diverse user inputs

**Steps**:
1. Test with simple input: "happy"
2. Test with complex input: "stressed from work but need to exercise"
3. Test with contextual input: "morning workout music"
4. Test with emotional input: "feeling nostalgic"
5. Test with specific input: "need pump-up songs for gym"
6. Test with vague input: "something good"
7. Test with new user (no history)
8. Test with existing user (has history)
9. For each, verify system produces appropriate playlist
10. Document system behavior for each input type

**Expected Output**: 
- All input types handled
- Simple inputs work
- Complex inputs parsed correctly
- Context understood
- Vague inputs handled gracefully
- User history utilized when available

**Verification Checklist**:
- [ ] Simple input works
- [ ] Complex input works
- [ ] Contextual input works
- [ ] Emotional input works
- [ ] Specific input works
- [ ] Vague input handled
- [ ] New user handled
- [ ] Existing user history used

---

### Subtask 5.6.3: Test Error Propagation

**Objective**: Verify error handling across agent pipeline

**Steps**:
1. Test Agent 1 failure (Ollama down)
   - Verify fallback mood parsing
   - Verify pipeline continues
2. Test Agent 2 failure (Spotify API down)
   - Verify error caught
   - Verify user notified clearly
3. Test Agent 3 failure (too few tracks)
   - Verify graceful handling
   - Verify best-effort playlist or clear error
4. Test database failure
   - Verify pipeline continues without history
5. Test Redis failure
   - Verify pipeline continues without cache
6. For each failure, verify:
   - No crashes
   - Clear error messages
   - Partial results if possible
   - Errors logged properly
7. Document error behavior

**Expected Output**: 
- All error scenarios handled
- No crashes
- Clear error messages
- Partial results when possible
- Error behavior documented

**Verification Checklist**:
- [ ] Agent 1 failure handled
- [ ] Agent 2 failure handled
- [ ] Agent 3 failure handled
- [ ] Database failure handled
- [ ] Redis failure handled
- [ ] No crashes in any scenario
- [ ] Error messages clear
- [ ] Errors logged

---

### Subtask 5.6.4: Benchmark Complete System Performance

**Objective**: Measure end-to-end system performance

**Steps**:
1. Run 20 test cases with various inputs
2. Measure total execution time for each
3. Calculate average execution time (target: 5-8 seconds)
4. Calculate p95 latency
5. Calculate p99 latency
6. Test with cache hits (should be 2-3 seconds)
7. Break down time by agent:
   - Agent 1: target 1-2s
   - Agent 2: target 3-5s
   - Agent 3: target 1-2s
8. Identify performance bottlenecks
9. Calculate cache hit rate
10. Document all performance metrics
11. Verify system meets requirements (<10s end-to-end)

**Expected Output**: 
- Performance metrics comprehensive
- Average time 5-8 seconds
- p95 and p99 acceptable
- Cache hits significantly faster
- Bottlenecks identified
- All metrics documented
- Requirements met

**Verification Checklist**:
- [ ] 20 test cases run
- [ ] Average time measured (<8s)
- [ ] p95 latency acceptable
- [ ] p99 latency acceptable
- [ ] Cache hit time <3s
- [ ] Agent 1 time ~1-2s
- [ ] Agent 2 time ~3-5s
- [ ] Agent 3 time ~1-2s
- [ ] Bottlenecks identified
- [ ] Cache hit rate measured
- [ ] All metrics documented
- [ ] Requirements met (<10s)

---

# PHASE 5 COMPLETION VERIFICATION

Before moving to Phase 6, verify all Phase 5 outputs:

**Tool 6: Track Ranking**:
- [ ] rank_tracks_by_relevance tool created
- [ ] Ranking algorithm implemented
- [ ] >80% top-10 relevance
- [ ] Wrapped as LangChain Tool

**Tool 7: Diversity**:
- [ ] optimize_diversity tool created
- [ ] Diversity constraints implemented
- [ ] Diversity score >70
- [ ] Wrapped as LangChain Tool

**Tool 8: Explanation**:
- [ ] generate_explanation tool created
- [ ] Uses LLM for natural language
- [ ] Templates for all moods
- [ ] Quality >4/5
- [ ] Wrapped as LangChain Tool

**Agent 3: Playlist Curator**:
- [ ] Agent created with ReAct pattern
- [ ] Configured with 3 tools
- [ ] Curation strategy logical
- [ ] Logging implemented

**Orchestration**:
- [ ] Orchestrator function created
- [ ] Agents connected sequentially
- [ ] Data flow implemented
- [ ] Orchestration logging in place

**Integration Testing**:
- [ ] Complete pipeline tested
- [ ] Various inputs handled
- [ ] Error propagation tested
- [ ] Performance benchmarked
- [ ] System meets requirements (<10s)

**Status**: Phase 5 ✅ COMPLETE - Ready for Phase 6

---

# PHASE 6: API Routes & Frontend with Streamlit (Days 6-7)

## Phase 6 Overview
This phase creates FastAPI endpoints to expose the multi-agent system and builds a Streamlit frontend for user interaction.

### Phase 6 Tasks & Subtasks
```
PHASE 6
├── TASK 6.1: FastAPI Routes for Multi-Agent System
│   ├── Subtask 6.1.1: Create POST /api/generate-playlist endpoint
│   ├── Subtask 6.1.2: Add request/response validation
│   ├── Subtask 6.1.3: Test endpoint with various inputs
│   └── Subtask 6.1.4: Document API endpoint
├── TASK 6.2: Additional API Routes
│   ├── Subtask 6.2.1: Create GET /api/users/{user_id}/playlists
│   ├── Subtask 6.2.2: Create POST /api/feedback
│   ├── Subtask 6.2.3: Create GET /api/mood-history
│   └── Subtask 6.2.4: Document all endpoints
├── TASK 6.3: Streamlit Frontend Setup
│   ├── Subtask 6.3.1: Create Streamlit app structure
│   ├── Subtask 6.3.2: Configure Streamlit settings
│   └── Subtask 6.3.3: Set up API client for Streamlit
├── TASK 6.4: Streamlit UI - Playlist Generation
│   ├── Subtask 6.4.1: Create mood input interface
│   ├── Subtask 6.4.2: Display generated playlist
│   ├── Subtask 6.4.3: Add Spotify links and metadata
│   └── Subtask 6.4.4: Add feedback buttons
├── TASK 6.5: Streamlit UI - User Dashboard & History
│   ├── Subtask 6.5.1: Create dashboard page
│   ├── Subtask 6.5.2: Display mood history with visualizations
│   ├── Subtask 6.5.3: Display playlist history
│   └── Subtask 6.5.4: Add analytics and insights
└── TASK 6.6: Frontend Testing
    ├── Subtask 6.6.1: Test UI functionality
    ├── Subtask 6.6.2: Test API integration
    ├── Subtask 6.6.3: Test on different screen sizes
    └── Subtask 6.6.4: Test end-to-end user workflow
```

**Note**: Due to length constraints, I'll provide a summary for Phases 6-10. The structure follows the same detailed pattern as Phases 1-5.

**Phase 6** covers:
- FastAPI endpoints exposing the 3-agent system
- Request/response validation with Pydantic
- Streamlit frontend with mood input, playlist display, and user history
- Complete UI testing and responsive design verification

**Phase 7** (Days 7-8): Containerization & Docker
- Backend and frontend Dockerfiles
- docker-compose.yml with all services
- Local Docker testing and optimization

**Phase 8** (Days 8-9): CI/CD Pipeline
- GitHub repository setup
- GitHub Actions workflows for testing
- Docker build and push to registry
- Automated deployment configuration

**Phase 9** (Day 9): Cloud Deployment
- Railway.app for backend
- Streamlit Cloud for frontend
- Cloud database and Redis setup
- Production monitoring and logging

**Phase 10** (Day 10): Final Verification & Documentation
- Code quality review and cleanup
- Complete testing summary
- Resume updates with project
- Portfolio presentation preparation
- Deployment documentation

---

# PROJECT COMPLETION CHECKLIST

## Final Verification Before Submission:

**Multi-Agent System**:
- [ ] 3 agents working independently
- [ ] 8 tools total (2+3+3) all functional
- [ ] Agents connected in pipeline
- [ ] Complete workflow: user input → final playlist
- [ ] Performance <10s end-to-end

**Production Quality**:
- [ ] Error handling at all levels
- [ ] Comprehensive logging
- [ ] Caching implemented (Redis)
- [ ] Database persistence (PostgreSQL)
- [ ] API documentation (Swagger)

**Deployment**:
- [ ] Backend deployed (Railway)
- [ ] Frontend deployed (Streamlit Cloud)
- [ ] CI/CD pipeline functional
- [ ] Monitoring active
- [ ] All services communicating

**Documentation**:
- [ ] README complete
- [ ] API documented
- [ ] Architecture documented
- [ ] Deployment guide complete
- [ ] Code comments present

**Portfolio Ready**:
- [ ] Resume updated
- [ ] Demo video/slides prepared
- [ ] GitHub repository clean
- [ ] Interview talking points ready

---

# 🎉 10-DAY ROADMAP COMPLETE

**This roadmap ensures**:
✅ Production-grade 3-agent AI system
✅ Real-world Spotify integration
✅ Comprehensive testing at every stage
✅ Full cloud deployment with CI/CD
✅ Portfolio-ready project for Mrsool interview

**Follow this roadmap step-by-step, verify each subtask, and you'll have an impressive agentic AI project in 10 days!**1. Create services/spotify/spotify_client.py
2. Define SpotifyClient class
3. Initialize with client_id and client_# MusicMood - 10 Day Implementation Roadmap (3-Agent AI System)
## Production-Grade Implementation with Comprehensive Verification

---

# IMPLEMENTATION GUIDELINES

## Core Principles:
1. **Verification After Each Subtask** - Move to next subtask only when current output is verified
2. **No Placeholder/Dummy Data** - Only production-grade, industry-level code
3. **Comprehensive Testing** - Rigorous testing at every workflow stage
4. **Phase Structure** - Phase → Task → Subtask with verification at each level
5. **Phase Start Protocol** - At start of each phase, review all tasks and subtasks before beginning
6. **Progress Tracking** - Refer to roadmap at end of each phase to verify completion status
7. **No Deviation** - Follow the roadmap strictly, do not skip or reorder

---

# PHASE 1: Local Environment Setup & Infrastructure (Days 1-2)

## Phase 1 Overview
This phase establishes the complete local development environment with all services running independently. Each service will be verified to work in isolation before integration.

### Phase 1 Tasks & Subtasks
```
PHASE 1
├── TASK 1.1: Ollama Local LLM Setup
│   ├── Subtask 1.1.1: Ollama installation and configuration
│   ├── Subtask 1.1.2: Download and verify Mistral model
│   └── Subtask 1.1.3: Test Ollama API endpoints
├── TASK 1.2: PostgreSQL Database Setup
│   ├── Subtask 1.2.1: PostgreSQL installation
│   ├── Subtask 1.2.2: Create database and user
│   └── Subtask 1.2.3: Verify connection and permissions
├── TASK 1.3: Redis Cache Setup
│   ├── Subtask 1.3.1: Redis installation
│   ├── Subtask 1.3.2: Configure Redis settings
│   └── Subtask 1.3.3: Test Redis connectivity
├── TASK 1.4: API Keys & Credentials Setup
│   ├── Subtask 1.4.1: Spotify API credentials
│   ├── Subtask 1.4.2: OpenWeatherMap API key
│   └── Subtask 1.4.3: Create .env file with all credentials
└── TASK 1.5: Python Virtual Environment & Dependencies
    ├── Subtask 1.5.1: Create virtual environment
    ├── Subtask 1.5.2: Install all pip dependencies
    └── Subtask 1.5.3: Verify all imports work
```

---

## TASK 1.1: Ollama Local LLM Setup

### Subtask 1.1.1: Ollama Installation and Configuration

**Objective**: Install Ollama and verify it runs as a service

**Steps**:
1. Download Ollama from ollama.ai (choose your OS: macOS/Linux/Windows)
2. Install and follow installation wizard
3. Verify Ollama service is running
4. Ensure Ollama listens on default port 11434
5. Check Ollama status via command line
6. Verify service auto-starts on system boot

**Expected Output**: 
- Ollama version number displays
- HTTP response 200 from localhost:11434
- Service running in background

**Verification Checklist**:
- [ ] Ollama installed successfully
- [ ] Service auto-starts on system boot
- [ ] Port 11434 is accessible
- [ ] No errors in system logs

---

### Subtask 1.1.2: Download and Verify Mistral Model

**Objective**: Download Mistral 7B model and ensure it loads correctly

**Steps**:
1. Pull Mistral model using Ollama CLI
2. Wait for download to complete (will take 5-10 minutes, approximately 4GB)
3. Verify model is listed in Ollama
4. Check model file integrity by loading it once
5. Test with simple prompt to verify response
6. Note the model size and parameters from output

**Expected Output**: 
- Model appears in Ollama list output
- Mistral responds to test prompt with coherent text
- No corruption errors during download
- Response time is reasonable (1-5 seconds for simple prompt)

**Verification Checklist**:
- [ ] Mistral model successfully downloaded
- [ ] Model listed with correct size
- [ ] Model loads and responds to prompts
- [ ] Response time is reasonable
- [ ] No CUDA/GPU errors (CPU mode is acceptable)

---

### Subtask 1.1.3: Test Ollama API Endpoints

**Objective**: Verify Ollama REST API works for programmatic access

**Steps**:
1. Start Ollama if not running
2. Test generate endpoint with a test request using curl or Postman
3. Use POST method to localhost:11434/api/generate
4. Send JSON body with model, prompt, and stream parameters
5. Verify response structure contains response field
6. Test with streaming disabled and enabled
7. Check response time and token generation
8. Test with invalid model name to verify error handling

**Expected Output**: 
- HTTP 200 response
- JSON response with required fields (response, model, created_at)
- Non-empty generated text
- Response time less than 10 seconds
- Proper error response for invalid model

**Verification Checklist**:
- [ ] Ollama API responds to POST requests
- [ ] Response format is valid JSON
- [ ] Generated text is coherent
- [ ] Streaming and non-streaming modes work
- [ ] Error handling works properly

---

## TASK 1.2: PostgreSQL Database Setup

### Subtask 1.2.1: PostgreSQL Installation

**Objective**: Install PostgreSQL and verify it runs as a service

**Steps**:
1. Download PostgreSQL from postgresql.org (version 15 or higher)
2. Install with default settings
3. Note the admin password set during installation
4. Verify installation by checking version
5. Start PostgreSQL service
6. Connect to default postgres database using psql or GUI client
7. Verify connection shows postgres prompt

**Expected Output**: 
- PostgreSQL version number displays
- Can connect to postgres database
- Database prompt appears without errors
- Service is running

**Verification Checklist**:
- [ ] PostgreSQL installed successfully
- [ ] Service is running
- [ ] Default postgres user can connect
- [ ] Port 5432 is listening

---

### Subtask 1.2.2: Create Database and User

**Objective**: Create a dedicated database and user for MusicMood

**Steps**:
1. Connect to postgres using admin credentials
2. Create new user with secure password for application
3. Create new database owned by the new user
4. Grant all privileges on database to new user
5. Connect to new database to verify access
6. Verify current user shows correctly
7. Test that new user has full privileges

**Expected Output**: 
- User creation success message
- Database creation success message
- Able to connect to musicmood database
- New user has appropriate permissions

**Verification Checklist**:
- [ ] Application user created successfully
- [ ] Application database created successfully
- [ ] User has full privileges on database
- [ ] Can switch to new database without errors
- [ ] Password authentication works

---

### Subtask 1.2.3: Verify Connection and Permissions

**Objective**: Test database connectivity with connection string

**Steps**:
1. Create connection string in proper format
2. Test connection using psql with full connection string
3. Create a test table to verify write permissions
4. Perform insert operation on test table
5. Perform select operation to verify read
6. Perform update operation to verify modification
7. Drop test table to verify delete permissions
8. Verify no privilege errors occur at any step

**Expected Output**: 
- Connection successful with connection string
- All CRUD operations succeed
- No permission denied errors
- Connection string format validated

**Verification Checklist**:
- [ ] Connection string works
- [ ] User can create tables
- [ ] User can insert data
- [ ] User can query data
- [ ] User can modify and delete data

---

## TASK 1.3: Redis Cache Setup

### Subtask 1.3.1: Redis Installation

**Objective**: Install Redis and verify it runs

**Steps**:
1. Download Redis from redis.io (version 7 or higher)
2. Install following OS-specific instructions
3. Verify installation by checking version
4. Start Redis server
5. In another terminal, test connection using redis-cli
6. Send PING command and verify PONG response
7. Check that Redis is listening on default port 6379

**Expected Output**: 
- Redis version number displays
- PONG response from redis-cli ping
- Service running without errors

**Verification Checklist**:
- [ ] Redis installed successfully
- [ ] Service starts without errors
- [ ] Port 6379 is listening
- [ ] redis-cli can connect

---

### Subtask 1.3.2: Configure Redis Settings

**Objective**: Configure Redis for production-like settings

**Steps**:
1. Locate redis.conf file (typically in /etc/redis/ or installation directory)
2. Set maxmemory to 512mb (sufficient for development)
3. Set maxmemory-policy to allkeys-lru for efficient eviction
4. Configure save settings for persistence
5. Restart Redis with configuration file
6. Verify settings applied using CONFIG GET command
7. Test that Redis respects memory limits

**Expected Output**: 
- Config file loads without errors
- CONFIG GET shows correct maxmemory value
- Redis starts with new settings
- Settings persist after restart

**Verification Checklist**:
- [ ] redis.conf located and readable
- [ ] maxmemory configured correctly
- [ ] maxmemory-policy configured
- [ ] Redis restarts with new config
- [ ] Settings persist after restart

---

### Subtask 1.3.3: Test Redis Connectivity

**Objective**: Verify Redis works for caching operations

**Steps**:
1. Connect to Redis using redis-cli
2. Test SET operation to store key-value pair
3. Test GET operation to retrieve value
4. Test DEL operation to delete key
5. Test expiration by setting key with TTL
6. Wait for expiration time and verify key is gone
7. Test list operations (LPUSH, LRANGE)
8. Test hash operations (HSET, HGET)
9. Verify all operations complete successfully

**Expected Output**: 
- All SET/GET/DEL operations succeed
- Key expires after set time
- List operations work correctly
- Hash operations work correctly

**Verification Checklist**:
- [ ] Can set and get key-value pairs
- [ ] Expiration works correctly
- [ ] List operations work
- [ ] Hash operations work
- [ ] No connection errors
- [ ] Data persists across commands

---

## TASK 1.4: API Keys & Credentials Setup

### Subtask 1.4.1: Spotify API Credentials

**Objective**: Obtain Spotify API credentials for music data access

**Steps**:
1. Go to developer.spotify.com
2. Create an account or log in with existing credentials
3. Navigate to Dashboard and create a new app
4. Fill in app name, description, and accept terms
5. Verify email if required
6. Copy Client ID and Client Secret to secure location
7. In app settings, add redirect URI for local development
8. Test credentials work by making test API call
9. Document rate limits from Spotify documentation

**Expected Output**: 
- Client ID (long alphanumeric string)
- Client Secret (long alphanumeric string)
- Redirect URI registered
- Credentials validated

**Verification Checklist**:
- [ ] Spotify app created successfully
- [ ] Client ID obtained
- [ ] Client Secret obtained
- [ ] Redirect URI configured
- [ ] Credentials stored securely (not in git)

---

### Subtask 1.4.2: OpenWeatherMap API Key

**Objective**: Obtain weather API key for context-aware recommendations

**Steps**:
1. Go to openweathermap.org
2. Create free account
3. Verify email address
4. Navigate to API keys section in dashboard
5. Default API key should be created automatically
6. Copy API key to secure location
7. Test API key by making sample weather API call
8. Check API response contains valid weather data
9. Document API rate limits for free tier

**Expected Output**: 
- API key (32-character string)
- Successful API response with weather data
- Rate limits documented
- Key validated

**Verification Checklist**:
- [ ] OpenWeatherMap account created
- [ ] API key generated
- [ ] API key allows requests
- [ ] Free tier plan is active
- [ ] Can retrieve weather data

---

### Subtask 1.4.3: Create .env File with All Credentials

**Objective**: Create secure environment file with all credentials

**Steps**:
1. In project root, create .env file
2. Add database connection string in proper format
3. Add Redis connection string
4. Add Ollama base URL (localhost:11434)
5. Add Spotify Client ID and Client Secret
6. Add OpenWeatherMap API key
7. Add any other environment-specific variables
8. Create .env.example with dummy values showing structure
9. Add .env to .gitignore to prevent accidental commit
10. Verify .env file is readable by Python

**Expected Output**: 
- .env file exists in project root
- Contains all required credentials in KEY=VALUE format
- .env.example shows correct structure
- File is not tracked by git

**Verification Checklist**:
- [ ] .env file created
- [ ] All credentials present
- [ ] Format is correct (KEY=VALUE)
- [ ] .env is in .gitignore
- [ ] .env.example shows structure but no real values
- [ ] Can be loaded by python-dotenv

---

## TASK 1.5: Python Virtual Environment & Dependencies

### Subtask 1.5.1: Create Virtual Environment

**Objective**: Set up isolated Python environment for project

**Steps**:
1. Navigate to project root directory
2. Create virtual environment using python venv module
3. Activate virtual environment (OS-specific command)
4. Verify activation by checking terminal prompt
5. Upgrade pip to latest version
6. Verify pip version is upgraded
7. Verify Python path points to virtual environment

**Expected Output**: 
- Virtual environment directory created
- Activation changes terminal prompt
- pip version is latest
- Python path shows venv

**Verification Checklist**:
- [ ] Virtual environment created successfully
- [ ] Can activate and deactivate
- [ ] Correct Python interpreter used from venv
- [ ] pip is upgraded
- [ ] No global packages affected

---

### Subtask 1.5.2: Install All Pip Dependencies

**Objective**: Install all required Python packages for backend and ML

**Steps**:
1. Create requirements.txt with all necessary packages:
   - FastAPI, Uvicorn (backend)
   - SQLAlchemy, psycopg2-binary (database)
   - Redis-py (caching)
   - LangChain, langchain-community (agents)
   - Transformers, sentence-transformers (embeddings)
   - Spotipy (Spotify API)
   - Python-dotenv (environment)
   - Pytest, pytest-cov (testing)
   - Additional utilities as needed
2. Install from requirements file
3. Wait for all packages to install (may take 5-10 minutes)
4. Verify no errors during installation
5. Check installed packages list
6. Note the versions of key packages
7. Verify package versions are compatible

**Expected Output**: 
- All packages install successfully
- No errors or warnings during installation
- Package list shows all expected packages
- Specific versions match requirements.txt

**Verification Checklist**:
- [ ] requirements.txt is production-grade
- [ ] All packages install without errors
- [ ] No conflicting package versions
- [ ] Can see all packages in pip list
- [ ] Virtual environment size is reasonable

---

### Subtask 1.5.3: Verify All Imports Work

**Objective**: Verify all installed packages can be imported without errors

**Steps**:
1. Start Python interpreter in virtual environment
2. Import and test each major package:
   - Import fastapi, check accessible
   - Import sqlalchemy, check version
   - Import transformers, verify models can be loaded
   - Import redis, test connection capability
   - Import langchain, check available
   - Import spotipy, check accessible
3. Exit interpreter
4. Create a simple test script that imports all packages
5. Run test script and verify no import errors
6. Verify no ModuleNotFoundError or similar errors
7. Document any version conflicts if found

**Expected Output**: 
- All imports succeed
- No ModuleNotFoundError or similar errors
- Versions match requirements.txt
- Test script runs without output (indicates success)

**Verification Checklist**:
- [ ] FastAPI imports successfully
- [ ] SQLAlchemy imports successfully
- [ ] Transformers library imports successfully
- [ ] Redis client imports successfully
- [ ] LangChain imports successfully
- [ ] All ML/AI libraries import successfully
- [ ] No missing dependency errors
- [ ] Can instantiate basic service classes

---

# PHASE 1 COMPLETION VERIFICATION

Before moving to Phase 2, verify all Phase 1 outputs:

**Ollama Services**:
- [ ] Ollama running on localhost:11434
- [ ] Mistral model loaded and responsive
- [ ] API endpoint tested and working

**Database Services**:
- [ ] PostgreSQL running on port 5432
- [ ] musicmood database created
- [ ] Application user with full privileges
- [ ] Connection string works

**Cache Services**:
- [ ] Redis running on port 6379
- [ ] Redis operations (SET/GET/DEL) working
- [ ] Memory configuration applied

**Credentials**:
- [ ] Spotify API credentials obtained
- [ ] OpenWeatherMap API key obtained
- [ ] .env file created with all secrets
- [ ] .env not tracked by git

**Python Environment**:
- [ ] Virtual environment active and working
- [ ] All dependencies installed
- [ ] All imports successful
- [ ] Test script runs without errors

**Status**: Phase 1 ✅ COMPLETE - Ready for Phase 2

---

# PHASE 2: Core Backend Architecture & Database Models (Days 2-3)

## Phase 2 Overview
This phase establishes the FastAPI backend structure, database models, and service layer. Each component will be tested in isolation with database integration.

### Phase 2 Tasks & Subtasks
```
PHASE 2
├── TASK 2.1: FastAPI Project Structure Setup
│   ├── Subtask 2.1.1: Create project directory structure
│   ├── Subtask 2.1.2: Initialize FastAPI application
│   └── Subtask 2.1.3: Configure CORS and middleware
├── TASK 2.2: Database Models & Schema
│   ├── Subtask 2.2.1: Create SQLAlchemy models for users
│   ├── Subtask 2.2.2: Create SQLAlchemy models for mood entries
│   ├── Subtask 2.2.3: Create SQLAlchemy models for playlists
│   └── Subtask 2.2.4: Run database migrations
├── TASK 2.3: Database Connection & Session Management
│   ├── Subtask 2.3.1: Configure database connection pooling
│   ├── Subtask 2.3.2: Create session factory
│   └── Subtask 2.3.3: Test database transactions
├── TASK 2.4: Environment Configuration Management
│   ├── Subtask 2.4.1: Create config.py for environment management
│   ├── Subtask 2.4.2: Load and validate environment variables
│   └── Subtask 2.4.3: Test configuration in different environments
└── TASK 2.5: Basic Health Check API
    ├── Subtask 2.5.1: Create health check endpoint
    ├── Subtask 2.5.2: Test health endpoint with database check
    └── Subtask 2.5.3: Document API response structure
```

---

## TASK 2.1: FastAPI Project Structure Setup

### Subtask 2.1.1: Create Project Directory Structure

**Objective**: Set up organized project directory layout following industry standards

**Steps**:
1. Create directory structure with clear separation of concerns
2. Create app/ directory (main application package)
3. Create agents/ directory for AI agents
4. Create tools/ directory for agent tools
5. Create models/ directory for database models
6. Create schemas/ directory for Pydantic request/response schemas
7. Create services/ directory for business logic
8. Create routes/ directory for API endpoints
9. Create utils/ directory for helper functions
10. Create tests/ directory for test files
11. Add __init__.py to all package directories

**Expected Output**: 
- Clean, organized directory structure
- Each module has __init__.py file
- Top-level main.py for application entry point
- Clear separation between agents, tools, and services

**Verification Checklist**:
- [ ] All required directories created
- [ ] Directory structure is logical and scalable
- [ ] __init__.py files present in all packages
- [ ] Agents and tools clearly separated
- [ ] No circular import issues

---

### Subtask 2.1.2: Initialize FastAPI Application

**Objective**: Create FastAPI app instance with proper configuration

**Steps**:
1. Create main.py in project root
2. Initialize FastAPI app with title, description, version
3. Set up logging configuration for application
4. Create application factory pattern if needed
5. Configure app metadata (title, version, description)
6. Initialize but do not start server yet
7. Verify app object can be created without errors
8. Add basic error handler for unhandled exceptions

**Expected Output**: 
- FastAPI application instance created
- Logging configured and working
- App metadata set correctly
- Basic error handling in place

**Verification Checklist**:
- [ ] FastAPI app initializes without errors
- [ ] App has correct title and version
- [ ] Logging is configured
- [ ] App can be imported in other modules
- [ ] No missing dependencies

---

### Subtask 2.1.3: Configure CORS and Middleware

**Objective**: Set up CORS for frontend access and security middleware

**Steps**:
1. Add CORS middleware with specific allowed origins
2. Configure allowed origins for localhost:3000 and localhost:8501
3. Configure allowed methods (GET, POST, PUT, DELETE)
4. Configure allowed headers (Authorization, Content-Type)
5. Add middleware for request/response logging
6. Add middleware for error handling
7. Test CORS preflight requests work
8. Verify middleware order is correct (CORS should be first)

**Expected Output**: 
- CORS configured without errors
- Middleware registered in correct order
- CORS headers present in responses
- Request/response logging working

**Verification Checklist**:
- [ ] CORS middleware added
- [ ] Allowed origins configured correctly
- [ ] Allowed methods set
- [ ] Logging middleware working
- [ ] Error handling middleware active
- [ ] No middleware conflicts

---

## TASK 2.2: Database Models & Schema

### Subtask 2.2.1: Create SQLAlchemy Models for Users

**Objective**: Define User model with all required fields

**Steps**:
1. Create User model in models/user.py
2. Include fields: id (primary key), username, email, created_at, updated_at
3. Add relationships to other models (mood_entries, playlist_history)
4. Add indexes on frequently queried columns (username, email)
5. Create BaseModel with common fields (id, created_at, updated_at)
6. Add table metadata and constraints (unique username, unique email)
7. Test model can be instantiated without errors
8. Add proper type hints for all fields

**Expected Output**: 
- User model defined with all fields
- Relationships configured
- Indexes created
- No validation errors
- Proper type hints

**Verification Checklist**:
- [ ] User model has all required fields
- [ ] Primary key defined
- [ ] Timestamps automatically managed
- [ ] Relationships defined correctly
- [ ] Indexes present on important columns
- [ ] Model can be reflected in database

---

### Subtask 2.2.2: Create SQLAlchemy Models for Mood Entries

**Objective**: Define MoodEntry model to store mood history

**Steps**:
1. Create MoodEntry model in models/mood.py
2. Include fields: id, user_id, mood_text, primary_mood, energy_level, emotional_intensity, context, mood_embedding, weather_context, time_of_day, created_at
3. Add foreign key relationship to User model
4. Add mood_embedding field as JSON type for storing embeddings
5. Add constraints to mood values (energy_level 1-10, intensity 1-10)
6. Add enum or check constraint for primary_mood valid values
7. Add indexes for queries (user_id, created_at)
8. Test model relationships work correctly

**Expected Output**: 
- MoodEntry model defined with all fields
- Foreign key relationship to User
- Mood values constrained to valid options
- Embedding storage as JSON configured

**Verification Checklist**:
- [ ] MoodEntry model created
- [ ] Foreign key to User configured
- [ ] All mood fields present
- [ ] Constraints defined properly
- [ ] Indexes created
- [ ] JSON field for embeddings configured

---

### Subtask 2.2.3: Create SQLAlchemy Models for Playlists

**Objective**: Define PlaylistRecommendation model to store generated playlists

**Steps**:
1. Create PlaylistRecommendation model in models/playlist.py
2. Include fields: id, user_id, spotify_song_ids (JSON array), generated_at, mood_entry_id, accuracy_score, user_rating, feedback_text
3. Add foreign keys to User and MoodEntry
4. Store song list as JSON array for flexibility
5. Add indexes for common queries (user_id, generated_at)
6. Add constraints for score ranges (accuracy_score 0-100, user_rating 0-5)
7. Configure cascade delete behavior
8. Test model relationships and cascading deletes work

**Expected Output**: 
- PlaylistRecommendation model defined
- Foreign keys to User and MoodEntry configured
- Song list stored as JSON
- Score validation constraints in place

**Verification Checklist**:
- [ ] PlaylistRecommendation model created
- [ ] Foreign keys configured
- [ ] JSON array for song IDs
- [ ] Score validation constraints
- [ ] Cascade delete behavior configured
- [ ] Relationships working correctly

---

### Subtask 2.2.4: Run Database Migrations

**Objective**: Create tables in PostgreSQL from models

**Steps**:
1. Import all models in models/__init__.py
2. Create migration script using Base.metadata.create_all()
3. Run migration script to create tables in database
4. Connect to database and verify tables exist
5. Check each table schema matches model definition
6. Verify columns have correct types and constraints
7. Verify foreign keys are created
8. Verify indexes are created
9. Test that models can be queried from database

**Expected Output**: 
- All tables created in PostgreSQL
- Correct column types and constraints
- Indexes visible in database
- Foreign keys established
- No migration errors

**Verification Checklist**:
- [ ] users table created with correct columns
- [ ] mood_entries table created
- [ ] playlist_recommendations table created
- [ ] Foreign keys created
- [ ] Indexes created
- [ ] Can query table schemas
- [ ] No orphaned or missing tables

---

## TASK 2.3: Database Connection & Session Management

### Subtask 2.3.1: Configure Database Connection Pooling

**Objective**: Set up efficient database connection pool for production use

**Steps**:
1. Create database.py with SQLAlchemy engine configuration
2. Configure engine with connection pooling (QueuePool)
3. Set pool size to 10 connections
4. Set max overflow to 20 for burst traffic
5. Add echo=False to reduce log verbosity
6. Configure connection timeout (30 seconds)
7. Test engine can connect to database
8. Verify pool management works correctly
9. Monitor connection pool metrics

**Expected Output**: 
- SQLAlchemy engine created with pool configuration
- Engine can establish connections
- Connection pooling active
- Pool size configured correctly

**Verification Checklist**:
- [ ] Engine created without errors
- [ ] Pool configured correctly
- [ ] Can establish test connection
- [ ] Connection timeout set
- [ ] Pool metrics accessible

---

### Subtask 2.3.2: Create Session Factory

**Objective**: Create session factory for database operations throughout app

**Steps**:
1. Create session factory using sessionmaker in database.py
2. Configure session to be tied to application lifecycle
3. Create get_db() dependency function for FastAPI
4. Add session scoping for thread safety
5. Configure session commit/rollback behavior
6. Test session creation and cleanup
7. Verify sessions are properly closed after use
8. Test session in FastAPI dependency injection

**Expected Output**: 
- SessionLocal factory created
- get_db() dependency function works
- Sessions created and closed properly
- No connection leaks

**Verification Checklist**:
- [ ] SessionLocal factory configured
- [ ] get_db() function works
- [ ] Sessions properly closed
- [ ] No connection leaks
- [ ] Thread-safe session handling

---

### Subtask 2.3.3: Test Database Transactions

**Objective**: Verify database transactions work correctly (commit, rollback)

**Steps**:
1. Create test script that opens a database session
2. Test successful transaction: insert data, commit, verify data persists
3. Test rollback: insert data, rollback, verify data is gone
4. Test transaction isolation: multiple sessions don't see uncommitted data
5. Test connection recovery: simulate connection error and retry
6. Verify session cleanup in all scenarios (success, error, exception)
7. Test nested transactions if needed
8. Verify no orphaned transactions remain

**Expected Output**: 
- Commits persist data correctly
- Rollbacks revert changes
- Transaction isolation works
- No orphaned transactions
- Connection recovery works

**Verification Checklist**:
- [ ] INSERT transactions work
- [ ] COMMIT persists data
- [ ] ROLLBACK removes changes
- [ ] Multiple sessions isolated
- [ ] Connection errors handled
- [ ] No session leaks

---

## TASK 2.4: Environment Configuration Management

### Subtask 2.4.1: Create Config.py for Environment Management

**Objective**: Centralize all environment-based configuration

**Steps**:
1. Create config/settings.py
2. Define Settings class using Pydantic BaseSettings
3. Group settings by category: database, redis, spotify, weather, ollama, app
4. Set default values for development environment
5. Configure to load from .env file automatically
6. Include validation for critical settings (URLs, API keys)
7. Test config can be loaded without errors
8. Add type hints for all settings

**Expected Output**: 
- Settings class created with all configuration groups
- Loads from .env correctly
- Provides defaults for development
- Validation rules in place

**Verification Checklist**:
- [ ] Settings class defined
- [ ] All required settings present
- [ ] Loads from .env file
- [ ] Environment variables override defaults
- [ ] Validation rules enforce required fields

---

### Subtask 2.4.2: Load and Validate Environment Variables

**Objective**: Ensure all required environment variables are present and valid

**Steps**:
1. On application startup, load and validate settings
2. Check all required API keys are present (Spotify, Weather)
3. Validate database URL format is correct
4. Validate Redis URL format is correct
5. Validate Ollama base URL is accessible
6. Log which environment is active (development/production)
7. Raise clear errors if critical settings missing
8. Test with missing .env file (should use defaults or error appropriately)

**Expected Output**: 
- Configuration loaded successfully
- All required variables present
- Environment set correctly
- Clear error messages if validation fails

**Verification Checklist**:
- [ ] .env file loaded
- [ ] All settings accessible
- [ ] Validation catches missing keys
- [ ] Error messages are clear
- [ ] Defaults used when appropriate
- [ ] No sensitive data in logs

---

### Subtask 2.4.3: Test Configuration in Different Environments

**Objective**: Verify configuration works in development and test environments

**Steps**:
1. Test with local .env file (development mode)
2. Test with environment variables only (production simulation)
3. Create test.env for testing environment
4. Verify settings switch correctly between environments
5. Verify sensitive data is not exposed in logs
6. Test configuration caching works
7. Test configuration reload if needed
8. Document environment-specific settings

**Expected Output**: 
- Configuration switches correctly between environments
- No hardcoded values in code
- Test configuration isolates from development
- Environment detection works

**Verification Checklist**:
- [ ] Development mode uses local .env
- [ ] Production mode uses environment variables
- [ ] Test mode uses test.env
- [ ] Configuration properly isolated
- [ ] No sensitive data exposed

---

## TASK 2.5: Basic Health Check API

### Subtask 2.5.1: Create Health Check Endpoint

**Objective**: Implement /api/health endpoint for monitoring

**Steps**:
1. Create routes/health.py
2. Define GET /api/health endpoint
3. Return JSON response with status, timestamp, version
4. Endpoint should have no authentication
5. Should be fast (less than 100ms response time)
6. Include service name in response
7. Test endpoint with curl or Postman

**Expected Output**: 
- GET /api/health returns 200 OK
- Response is valid JSON with status field
- Response time less than 100ms
- Includes timestamp and version

**Verification Checklist**:
- [ ] Endpoint defined and working
- [ ] Returns correct JSON structure
- [ ] Status code is 200
- [ ] Fast response time
- [ ] No errors in response

---

### Subtask 2.5.2: Test Health Endpoint with Database Check

**Objective**: Extend health check to verify database connectivity

**Steps**:
1. Modify /api/health to include database connectivity check
2. Execute simple query to verify database working
3. Return database status in response (healthy/unhealthy)
4. Include Redis connectivity check
5. Return overall health status (healthy/degraded/unhealthy)
6. Test with database running and stopped
7. Verify appropriate status returned in each case
8. Add timeout to database check (5 seconds)

**Expected Output**: 
- Health endpoint checks database
- Response includes database status
- Returns 200 if all services healthy
- Returns 503 if services degraded
- Clear status messages

**Verification Checklist**:
- [ ] Database connectivity checked
- [ ] Redis connectivity checked
- [ ] Returns appropriate HTTP status
- [ ] Response time still reasonable
- [ ] Works with services up and down
- [ ] Clear status information

---

### Subtask 2.5.3: Document API Response Structure

**Objective**: Document health endpoint response and integrate with FastAPI docs

**Steps**:
1. Define Pydantic response model for health check
2. Add to FastAPI route with response_model parameter
3. Add endpoint documentation with description and tags
4. Add examples of successful and failed health checks
5. Verify FastAPI Swagger documentation shows endpoint
6. Test Swagger UI at /docs displays correctly
7. Verify endpoint shows in ReDoc at /redoc
8. Document response schema clearly with field descriptions

**Expected Output**: 
- Health endpoint documented in Swagger
- Response schema visible in /docs and /redoc
- Clear descriptions of all response fields
- Examples provided

**Verification Checklist**:
- [ ] Pydantic response model created
- [ ] FastAPI documentation generated
- [ ] Swagger UI shows endpoint
- [ ] ReDoc shows endpoint
- [ ] Response schema is clear
- [ ] All fields documented with descriptions

---

# PHASE 2 COMPLETION VERIFICATION

Before moving to Phase 3, verify all Phase 2 outputs:

**Project Structure**:
- [ ] Directory structure organized and scalable
- [ ] All required packages created including agents/ and tools/
- [ ] __init__.py files present

**FastAPI Application**:
- [ ] App initializes without errors
- [ ] CORS configured correctly
- [ ] Middleware in correct order
- [ ] Logging working

**Database Models**:
- [ ] User table created with correct schema
- [ ] MoodEntry table created
- [ ] PlaylistRecommendation table created
- [ ] Foreign keys configured
- [ ] Indexes created

**Database Connection**:
- [ ] Connection pooling configured
- [ ] SessionLocal factory works
- [ ] Transactions commit/rollback correctly
- [ ] No connection leaks

**Configuration**:
- [ ] Settings class loads from .env
- [ ] All required variables present
- [ ] Environment-specific configs work
- [ ] No hardcoded secrets in code

**Health Endpoint**:
- [ ] GET /api/health returns 200
- [ ] Database connectivity checked
- [ ] Redis connectivity checked
- [ ] Response includes service status
- [ ] Documented in Swagger

**Status**: Phase 2 ✅ COMPLETE - Ready for Phase 3

---

# PHASE 3: Multi-Agent System - Agent 1 (Mood Understanding) (Day 3)

## Phase 3 Overview
This phase implements the first agent of the 3-agent system: the Mood Understanding Agent. This agent analyzes user input and extracts structured mood data using LangChain and Ollama.

### Phase 3 Tasks & Subtasks
```
PHASE 3
├── TASK 3.1: LangChain Setup & Integration
│   ├── Subtask 3.1.1: Install and configure LangChain
│   ├── Subtask 3.1.2: Integrate Ollama with LangChain
│   └── Subtask 3.1.3: Test LangChain-Ollama connection
├── TASK 3.2: Agent 1 Tools - Mood Parsing
│   ├── Subtask 3.2.1: Create parse_mood_with_llm tool
│   ├── Subtask 3.2.2: Test mood parsing with various inputs
│   └── Subtask 3.2.3: Add error handling and fallbacks
├── TASK 3.3: Agent 1 Tools - User Context
│   ├── Subtask 3.3.1: Create get_user_context tool
│   ├── Subtask 3.3.2: Implement user preference retrieval
│   └── Subtask 3.3.3: Test context retrieval from database
├── TASK 3.4: Build Agent 1 with ReAct Pattern
│   ├── Subtask 3.4.1: Create Mood Understanding Agent
│   ├── Subtask 3.4.2: Configure agent with tools
│   ├── Subtask 3.4.3: Test agent reasoning and tool selection
│   └── Subtask 3.4.4: Add agent logging and monitoring
└── TASK 3.5: Agent 1 Integration Testing
    ├── Subtask 3.5.1: Test with simple mood inputs
    ├── Subtask 3.5.2: Test with complex mood descriptions
    ├── Subtask 3.5.3: Test error scenarios
    └── Subtask 3.5.4: Benchmark Agent 1 performance
```

---

## TASK 3.1: LangChain Setup & Integration

### Subtask 3.1.1: Install and Configure LangChain

**Objective**: Install LangChain and verify basic functionality

**Steps**:
1. Ensure virtual environment is active
2. Install langchain and langchain-community packages
3. Verify installation by importing langchain
4. Check LangChain version is compatible (0.1.0 or higher)
5. Install additional LangChain dependencies as needed
6. Review LangChain documentation for agents and tools
7. Create langchain_config.py for LangChain-specific settings

**Expected Output**: 
- LangChain installed successfully
- Can import langchain modules
- Version compatible
- Configuration file created

**Verification Checklist**:
- [ ] LangChain packages installed
- [ ] Can import langchain modules
- [ ] Version is 0.1.0 or higher
- [ ] Dependencies resolved
- [ ] Configuration file created

---

### Subtask 3.1.2: Integrate Ollama with LangChain

**Objective**: Connect LangChain to local Ollama instance

**Steps**:
1. Import Ollama LLM from langchain-community
2. Create Ollama LLM instance pointing to localhost:11434
3. Specify model name as "mistral"
4. Configure temperature, max_tokens, and other parameters
5. Test LLM can generate simple response
6. Verify response is coherent and relevant
7. Test with different prompts to ensure consistency
8. Document Ollama LLM configuration

**Expected Output**: 
- Ollama LLM instance created
- Can generate text responses
- Responses are coherent
- Configuration documented

**Verification Checklist**:
- [ ] Ollama LLM instance created
- [ ] Connected to localhost:11434
- [ ] Model "mistral" loaded
- [ ] Can generate responses
- [ ] Responses are coherent

---

### Subtask 3.1.3: Test LangChain-Ollama Connection

**Objective**: Verify LangChain can reliably call Ollama

**Steps**:
1. Create test script to invoke Ollama via LangChain
2. Test with simple prompt: "What is AI?"
3. Verify response is received
4. Test with structured prompt requiring JSON output
5. Verify Ollama respects prompt instructions
6. Test error handling when Ollama is unavailable
7. Test timeout behavior (set 30 second timeout)
8. Measure average response time for simple prompts
9. Document connection reliability

**Expected Output**: 
- LangChain successfully calls Ollama
- Responses received in 1-3 seconds
- Structured prompts work
- Error handling functional
- Timeouts enforced

**Verification Checklist**:
- [ ] Simple prompts work
- [ ] Structured prompts work
- [ ] Response time acceptable (1-3s)
- [ ] Error handling works
- [ ] Timeout enforced
- [ ] Connection reliable

---

## TASK 3.2: Agent 1 Tools - Mood Parsing

### Subtask 3.2.1: Create parse_mood_with_llm Tool

**Objective**: Build first tool for mood parsing using LLM

**Steps**:
1. Create tools/mood_tools.py file
2. Define parse_mood_with_llm function
3. Function accepts user mood text as input
4. Craft prompt that extracts:
   - primary_mood (happy, sad, energetic, calm, focus, stressed, etc.)
   - energy_level (1-10 scale)
   - emotional_intensity (1-10 scale)
   - context (work, gym, sleep, party, study, etc.)
5. Use Ollama LLM to process prompt
6. Parse LLM response into structured dictionary
7. Add validation for parsed values (ranges, types)
8. Return structured mood data
9. Wrap function as LangChain Tool with proper name and description

**Expected Output**: 
- parse_mood_with_llm tool created
- Returns structured mood data
- Validation in place
- Wrapped as LangChain Tool

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts mood text input
- [ ] Returns structured dictionary
- [ ] primary_mood extracted
- [ ] energy_level (1-10) extracted
- [ ] emotional_intensity (1-10) extracted
- [ ] context extracted
- [ ] Validation checks values
- [ ] Wrapped as LangChain Tool

---

### Subtask 3.2.2: Test Mood Parsing with Various Inputs

**Objective**: Verify mood parsing works for diverse inputs

**Steps**:
1. Create test suite for mood parsing tool
2. Test case 1: Simple mood - "I'm happy"
   - Expected: {primary_mood: "happy", energy: 7-8, intensity: 6-7}
3. Test case 2: Complex mood - "I'm stressed about work but trying to focus"
   - Expected: {primary_mood: "focus" or "stressed", energy: 5-6, context: "work"}
4. Test case 3: Contextual - "Just woke up, need gentle music"
   - Expected: {primary_mood: "calm", energy: 3-5, context: "morning"}
5. Test case 4: Activity-based - "At the gym, need pump up songs"
   - Expected: {primary_mood: "energetic", energy: 8-10, context: "gym"}
6. Test case 5: Emotional - "Feeling down after a tough day"
   - Expected: {primary_mood: "sad", intensity: 6-8, context: "work"}
7. Verify parsed data matches expected ranges
8. Document any parsing inconsistencies
9. Refine prompt if needed for better accuracy

**Expected Output**: 
- All test cases produce reasonable results
- primary_mood matches intent
- energy/intensity levels appropriate
- Context correctly identified
- Parsing accuracy >85%

**Verification Checklist**:
- [ ] Simple moods parsed correctly
- [ ] Complex moods parsed correctly
- [ ] Context extracted from input
- [ ] Energy levels reasonable
- [ ] Intensity levels reasonable
- [ ] Parsing accuracy >85%

---

### Subtask 3.2.3: Add Error Handling and Fallbacks

**Objective**: Make mood parsing tool robust with fallbacks

**Steps**:
1. Add try-catch block around LLM call
2. Handle Ollama connection errors gracefully
3. Handle invalid LLM responses (non-JSON, missing fields)
4. Implement fallback: if LLM fails, use basic keyword matching
5. Fallback should extract mood from common words (happy, sad, energetic, etc.)
6. Set default values for missing fields
7. Log all errors with context
8. Add timeout (30 seconds) to LLM call
9. Test error handling by stopping Ollama
10. Test timeout by using very long prompt
11. Verify fallback provides reasonable default mood

**Expected Output**: 
- Tool handles errors gracefully
- Fallback mood parsing works
- No unhandled exceptions
- Logs errors clearly
- Timeout enforced

**Verification Checklist**:
- [ ] Connection errors caught
- [ ] Invalid responses handled
- [ ] Fallback parsing works
- [ ] Default values provided
- [ ] Errors logged clearly
- [ ] Timeout enforced
- [ ] No crashes on error

---

## TASK 3.3: Agent 1 Tools - User Context

### Subtask 3.3.1: Create get_user_context Tool

**Objective**: Build tool to retrieve user's historical data

**Steps**:
1. In tools/mood_tools.py, define get_user_context function
2. Function accepts user_id and current time as inputs
3. Query database for user's past mood entries (last 10 moods)
4. Query database for user's listening preferences if available
5. Calculate user's average energy level from history
6. Calculate user's average emotional intensity from history
7. Identify user's most common contexts (work, gym, etc.)
8. Structure data as dictionary with past_moods, preferences, statistics
9. Wrap function as LangChain Tool with proper description
10. Add caching with Redis (TTL 30 minutes)

**Expected Output**: 
- get_user_context tool created
- Retrieves user's historical data
- Calculates statistics
- Cached for performance
- Wrapped as LangChain Tool

**Verification Checklist**:
- [ ] Tool function defined
- [ ] Accepts user_id input
- [ ] Queries database for mood history
- [ ] Retrieves preferences
- [ ] Calculates statistics
- [ ] Returns structured dictionary
- [ ] Caching implemented
- [ ] Wrapped as LangChain Tool

---

### Subtask 3.3.2: Implement User Preference Retrieval

**Objective**: Extract and structure user preferences

**Steps**:
1. Query database for user's past playlists
2. Extract most common genres from past playlists
3. Extract most common artists from past playlists
4. Identify patterns in energy levels user prefers
5. Identify patterns in contexts user listens in
6. Calculate average playlist ratings if available
7. Structure preferences as dictionary
8. Handle new users with no history gracefully
9. Return default preferences for new users

**Expected Output**: 
- User preferences extracted from history
- Common genres, artists identified
- Patterns recognized
- New users handled gracefully
- Default preferences provided

**Verification Checklist**:
- [ ] Preferences extracted from database
- [ ] Genres identified
- [ ] Artists identified
- [ ] Patterns recognized
- [ ] New users handled
- [ ] Default preferences provided

---

### Subtask 3.3.3: Test Context Retrieval from Database

**Objective**: Verify user context tool works correctly

**Steps**:
1. Create test user in database
2. Insert sample mood entries for test user
3. Insert sample playlists for test user
4. Call get_user_context tool with test user_id
5. Verify past moods are retrieved correctly
6. Verify preferences are calculated correctly
7. Verify statistics are accurate
8. Test with new user (no history)
9. Verify default values returned for new user
10. Test caching: second call should be faster
11. Test cache expiration after TTL

**Expected Output**: 
- Context retrieved for existing user
- Past moods accurate
- Preferences accurate
- New user returns defaults
- Caching improves performance
- Cache expires correctly

**Verification Checklist**:
- [ ] Retrieves data for existing user
- [ ] Past moods correct
- [ ] Preferences correct
- [ ] Statistics accurate
- [ ] New user handled
- [ ] Caching works (second call faster)
- [ ] Cache expires after TTL

---

## TASK 3.4: Build Agent 1 with ReAct Pattern

### Subtask 3.4.1: Create Mood Understanding Agent

**Objective**: Build Agent 1 using LangChain's ReAct pattern

**Steps**:
1. Create agents/mood_agent.py file
2. Import create_react_agent from LangChain
3. Define agent prompt template for mood understanding
4. Prompt should instruct agent to:
   - Use parse_mood_with_llm tool to analyze user input
   - Use get_user_context tool to understand user preferences
   - Think step-by-step (ReAct pattern)
   - Return structured mood data
5. Create list of tools for agent (2 tools)
6. Create agent using create_react_agent with Ollama LLM and tools
7. Configure agent with proper prompt
8. Test agent can be instantiated without errors

**Expected Output**: 
- Mood Understanding Agent created
- Uses ReAct pattern for reasoning
- Has access to 2 tools
- Prompt configured correctly
- Agent instantiates successfully

**Verification Checklist**:
- [ ] Agent file created
- [ ] Agent uses ReAct pattern
- [ ] Prompt template defined
- [ ] 2 tools provided to agent
- [ ] Agent created successfully
- [ ] No instantiation errors

---

### Subtask 3.4.2: Configure Agent with Tools

**Objective**: Properly configure agent with tools and executor

**Steps**:
1. Create AgentExecutor wrapping the agent
2. Pass tools list to executor
3. Configure max_iterations (set to 3)
4. Configure verbose mode for debugging
5. Enable handle_parsing_errors for robustness
6. Enable return_intermediate_steps for transparency
7. Set timeout for agent execution (30 seconds)
8. Test executor can be invoked
9. Verify executor returns result

**Expected Output**: 
- AgentExecutor configured
- Max iterations set
- Verbose logging enabled
- Error handling enabled
- Timeout configured
- Executor works

**Verification Checklist**:
- [ ] AgentExecutor created
- [ ] Tools provided to executor
- [ ] max_iterations set to 3
- [ ] verbose=True for logging
- [ ] handle_parsing_errors=True
- [ ] Timeout configured
- [ ] Can invoke executor

---

### Subtask 3.4.3: Test Agent Reasoning and Tool Selection

**Objective**: Verify agent makes intelligent decisions about tool usage

**Steps**:
1. Invoke agent with simple mood: "I'm happy"
2. Observe agent's reasoning process (check logs)
3. Verify agent calls parse_mood_with_llm tool
4. Verify agent produces structured mood output
5. Invoke agent with user_id provided
6. Verify agent also calls get_user_context tool
7. Check agent combines mood data with user context
8. Test agent's decision-making: does it use tools appropriately?
9. Verify agent doesn't make unnecessary tool calls
10. Test agent handles tool failures gracefully

**Expected Output**: 
- Agent reasons step-by-step
- Calls appropriate tools
- Combines information from multiple tools
- Makes intelligent decisions
- Handles tool failures

**Verification Checklist**:
- [ ] Agent calls parse_mood_with_llm
- [ ] Agent calls get_user_context when user_id provided
- [ ] Agent reasoning is logical
- [ ] Agent doesn't make unnecessary calls
- [ ] Agent combines tool outputs
- [ ] Agent handles tool errors

---

### Subtask 3.4.4: Add Agent Logging and Monitoring

**Objective**: Implement logging for agent execution

**Steps**:
1. Add structured logging to agent execution
2. Log when agent starts execution
3. Log each tool call with tool name and inputs
4. Log tool responses
5. Log agent's reasoning steps
6. Log final output
7. Log execution time for agent
8. Log any errors that occur
9. Create log format that's easy to parse
10. Test logging captures all relevant information
11. Verify logs don't expose sensitive data

**Expected Output**: 
- Comprehensive logging implemented
- All agent actions logged
- Execution time tracked
- Errors logged with context
- No sensitive data in logs

**Verification Checklist**:
- [ ] Agent execution logged
- [ ] Tool calls logged
- [ ] Tool responses logged
- [ ] Reasoning steps logged
- [ ] Execution time logged
- [ ] Errors logged
- [ ] No sensitive data exposed

---

## TASK 3.5: Agent 1 Integration Testing

### Subtask 3.5.1: Test with Simple Mood Inputs

**Objective**: Test Agent 1 with straightforward mood descriptions

**Steps**:
1. Test input: "I'm happy"
   - Verify agent returns: {primary_mood: "happy", energy: 7-8}
2. Test input: "I'm tired"
   - Verify agent returns: {primary_mood: "calm", energy: 2-4}
3. Test input: "I'm energetic"
   - Verify agent returns: {primary_mood: "energetic", energy: 8-10}
4. Test input: "I'm sad"
   - Verify agent returns: {primary_mood: "sad", intensity: 6-8}
5. Test input: "I need focus"
   - Verify agent returns: {primary_mood: "focus", energy: 5-7}
6. For each test, verify agent uses parse_mood_with_llm tool
7. For each test, verify output structure is correct
8. Document any unexpected results

**Expected Output**: 
- All simple moods parsed correctly
- Agent behavior consistent
- Output structure correct
- Parsing accuracy high

**Verification Checklist**:
- [ ] "Happy" mood parsed correctly
- [ ] "Tired" mood parsed correctly
- [ ] "Energetic" mood parsed correctly
- [ ] "Sad" mood parsed correctly
- [ ] "Focus" mood parsed correctly
- [ ] Output structure consistent
- [ ] Parsing accuracy >90%

---

### Subtask 3.5.2: Test with Complex Mood Descriptions

**Objective**: Test Agent 1 with nuanced, complex inputs

**Steps**:
1. Test input: "I had a stressful day at work but now I need to relax"
   - Verify context: "work" extracted
   - Verify primary_mood: "calm" or "stressed"
   - Verify agent understands the shift (stressed → relax)
2. Test input: "Going for a morning run, need motivational songs"
   - Verify context: "gym" or "exercise"
   - Verify energy: 8-10
   - Verify time: "morning" if extracted
3. Test input: "Late night coding session, need to stay focused"
   - Verify primary_mood: "focus"
   - Verify context: "work"
   - Verify energy: 6-7 (focused but not hyper)
4. Test input: "Feeling nostalgic about college days"
   - Verify primary_mood: "nostalgic" or "calm"
   - Verify emotional_intensity captures the feeling
5. Test input: "Breaking up with partner, need emotional songs"
   - Verify primary_mood: "sad"
   - Verify high emotional_intensity
6. For each, verify agent calls both tools appropriately
7. For each, verify context is extracted correctly

**Expected Output**: 
- Complex moods parsed accurately
- Context extracted correctly
- Agent handles nuanced descriptions
- Multi-faceted moods captured

**Verification Checklist**:
- [ ] Work stress mood parsed
- [ ] Morning run mood parsed
- [ ] Late night coding mood parsed
- [ ] Nostalgic mood parsed
- [ ] Emotional mood parsed
- [ ] Context extracted in each case
- [ ] Nuances captured

---

### Subtask 3.5.3: Test Error Scenarios

**Objective**: Verify Agent 1 handles errors gracefully

**Steps**:
1. Test with Ollama stopped (simulate LLM failure)
   - Verify agent uses fallback mood parsing
   - Verify agent doesn't crash
   - Verify reasonable default mood returned
2. Test with invalid user_id (non-existent user)
   - Verify agent handles gracefully
   - Verify default user context returned
3. Test with empty mood input
   - Verify agent handles or requests clarification
   - Verify no crashes
4. Test with very long mood description (1000+ characters)
   - Verify timeout doesn't occur
   - Verify agent processes or truncates
5. Test with database connection failure
   - Verify agent can still parse mood (without context)
   - Verify error logged
6. Test with Redis cache failure
   - Verify agent falls back to database query
   - Verify functionality maintained
7. For each error, verify logs capture the issue
8. For each error, verify agent produces some output (doesn't fail completely)

**Expected Output**: 
- All error scenarios handled gracefully
- No complete failures
- Fallbacks work
- Errors logged clearly
- Reasonable defaults provided

**Verification Checklist**:
- [ ] LLM failure handled
- [ ] Invalid user_id handled
- [ ] Empty input handled
- [ ] Long input handled
- [ ] Database failure handled
- [ ] Redis failure handled
- [ ] All errors logged
- [ ] No complete failures

---

### Subtask 3.5.4: Benchmark Agent 1 Performance

**Objective**: Measure and document Agent 1 performance metrics

**Steps**:
1. Run 10 test cases with simple moods
2. Measure average execution time (target: 1-2 seconds)
3. Measure p95 latency (95th percentile)
4. Measure p99 latency (99th percentile)
5. Run 10 test cases with complex moods
6. Measure average execution time (target: 2-3 seconds)
7. Test with user context retrieval
8. Measure impact of context retrieval on latency
9. Test cache hit scenario
10. Measure cache hit latency (should be <500ms)
11. Document all metrics in table format
12. Identify any performance bottlenecks
13. Verify performance meets requirements (simple: <2s, complex: <3s)

**Expected Output**: 
- Performance metrics documented
- Simple moods: avg 1-2s
- Complex moods: avg 2-3s
- Cache hits: <500ms
- p95 and p99 latencies acceptable
- Bottlenecks identified if any

**Verification Checklist**:
- [ ] Simple mood latency measured (avg <2s)
- [ ] Complex mood latency measured (avg <3s)
- [ ] p95 latency acceptable
- [ ] p99 latency acceptable
- [ ] Cache hit latency <500ms
- [ ] Metrics documented
- [ ] Performance meets requirements

---

# PHASE 3 COMPLETION VERIFICATION

Before moving to Phase 4, verify all Phase 3 outputs:

**LangChain Setup**:
- [ ] LangChain installed and configured
- [ ] Ollama integrated with LangChain
- [ ] Connection tested and reliable

**Tool 1: Mood Parsing**:
- [ ] parse_mood_with_llm tool created
- [ ] Works with various inputs
- [ ] Error handling and fallbacks in place
- [ ] Wrapped as LangChain Tool

**Tool 2: User Context**:
- [ ] get_user_context tool created
- [ ] Retrieves user history from database
- [ ] Calculates preferences and statistics
- [ ] Caching implemented
- [ ] Wrapped as LangChain Tool

**Agent 1: Mood Understanding**:
- [ ] Agent created with ReAct pattern
- [ ] Configured with 2 tools
- [ ] AgentExecutor configured properly
- [ ] Reasoning and tool selection works
- [ ] Logging and monitoring in place

**Testing**:
- [ ] Simple moods parsed correctly
- [ ] Complex moods parsed correctly
- [ ] Error scenarios handled
- [ ] Performance benchmarked
- [ ] Metrics within requirements

**Status**: Phase 3 ✅ COMPLETE - Ready for Phase 4

---

# PHASE 4: Multi-Agent System - Agent 2 (Music Discovery) (Day 4)

## Phase 4 Overview
This phase implements the second agent: the Music Discovery Agent. This agent searches Spotify for candidate tracks, retrieves audio features, and filters based on mood requirements.

### Phase 4 Tasks & Subtasks
```
PHASE 4
├── TASK 4.1: Spotify API Client Setup
│   ├── Subtask 4.1.1: Create SpotifyClient wrapper class
│   ├── Subtask 4.1.2: Implement authentication (client credentials flow)
│   ├── Subtask 4.1.3: Test API connection and rate limiting
│   └── Subtask 4.1.4: Implement error handling for API failures
├── TASK 4.2: Agent 2 Tools - Spotify Search
│   ├── Subtask 4.2.1: Create search_spotify_by_mood tool
│   ├── Subtask 4.2.2: Implement intelligent query generation
│   ├── Subtask 4.2.3: Test search with various moods
│   └── Subtask 4.2.4: Add search result caching
├── TASK 4.3: Agent 2 Tools - Audio Analysis
│   ├── Subtask 4.3.1: Create get_audio_features_batch tool
│   ├── Subtask 4.3.2: Implement batch processing
│   └── Subtask 4.3.3: Add feature caching
├── TASK 4.4: Agent 2 Tools - Track Filtering
│   ├── Subtask 4.4.1: Create filter_tracks_by_criteria tool
│   ├── Subtask 4.4.2: Implement filtering logic
│   └── Subtask 4.4.3: Test filtering accuracy
├── TASK 4.5: Build Agent 2 with ReAct Pattern
│   ├── Subtask 4.5.1: Create Music Discovery Agent
│   ├── Subtask 4.5.2: Configure agent with 3 tools
│   ├── Subtask 4.5.3: Test agent search strategy
│   └── Subtask 4.5.4: Add agent logging
└── TASK 4.6: Agent 2 Integration Testing
    ├── Subtask 4.6.1: Test end-to-end discovery process
    ├── Subtask 4.6.2: Test with various mood types
    ├── Subtask 4.6.3: Test error handling
    └── Subtask 4.6.4: Benchmark Agent 2 performance
```

---

## TASK 4.1: Spotify API Client Setup

### Subtask 4.1.1: Create SpotifyClient Wrapper Class

**Objective**: Create production-grade Spotify API client

**Steps**:
1. Create services/spotify/spotify_client.py
2. Define SpotifyClient class
3. Initialize with client_id and client_secret from config
4. Add