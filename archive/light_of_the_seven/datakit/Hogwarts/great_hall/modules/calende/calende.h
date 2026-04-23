#ifndef GREAT_HALL_CALENDE_H
#define GREAT_HALL_CALENDE_H

/*
  calende.h — Great Hall "calende" module (C)
  Purpose:
    - Session agenda: items, timeboxes, ordering
    - Milestones: due dates, reminders, ownership
    - Emits/consumes JSON documents compatible with Great Hall shared contract

  Design notes:
    - This is a skeleton header. Implementations should be in calende.c.
    - Memory ownership is explicit: functions document who allocates/frees.
    - JSON is treated as UTF-8 text; a JSON library can be integrated in calende.c.

  Thread-safety:
    - Instances are not thread-safe unless the implementation states otherwise.
*/

#include <stddef.h> /* size_t */

#ifdef __cplusplus
extern "C" {
#endif

/* ---------------------------- Versioning ---------------------------- */

#define GH_CALENDE_VERSION_MAJOR 1
#define GH_CALENDE_VERSION_MINOR 0
#define GH_CALENDE_VERSION_PATCH 0

/* ----------------------------- Status ------------------------------ */

typedef enum gh_calende_status {
  GH_CALENDE_OK = 0,
  GH_CALENDE_ERR_INVALID_ARGUMENT = 1,
  GH_CALENDE_ERR_OUT_OF_MEMORY = 2,
  GH_CALENDE_ERR_PARSE = 3,
  GH_CALENDE_ERR_NOT_FOUND = 4,
  GH_CALENDE_ERR_IO = 5,
  GH_CALENDE_ERR_BUFFER_TOO_SMALL = 6,
  GH_CALENDE_ERR_INTERNAL = 100
} gh_calende_status_t;

/* Convert a status code to a stable string literal (never NULL). */
const char* gh_calende_status_str(gh_calende_status_t status);

/* ----------------------------- Time ------------------------------- */

/*
  RFC3339 timestamps are carried as strings (UTF-8), e.g.:
    "2025-12-14T01:23:45Z"
  calende does not mandate parsing; it can, if the implementation chooses.
*/
typedef struct gh_rfc3339 {
  const char* s; /* Not owned unless explicitly copied into module storage. */
} gh_rfc3339_t;

/* ------------------------- Core concepts -------------------------- */

typedef enum gh_vibe {
  GH_VIBE_CALM_DIRECT = 0,
  GH_VIBE_NERVOUS_HIGH_STAKES = 1,
  GH_VIBE_EXPLORATORY_PLAYFUL = 2,
  GH_VIBE_ANALYTICAL_METHODICAL = 3,
  GH_VIBE_RESTORATIVE_REPAIR = 4,
  GH_VIBE_CUSTOM = 5
} gh_vibe_t;

/* Agenda item: a single timeboxed unit of discussion. */
typedef struct gh_agenda_item {
  char* item_id;            /* stable ID (owned by agenda) */
  char* title;              /* short label (owned by agenda) */
  char* description;        /* optional (owned by agenda, may be NULL) */

  /* Optional timebox in minutes; 0 means "unset". */
  unsigned int timebox_minutes;

  /* Optional ordering hint. Lower first; 0 means "unspecified". */
  unsigned int order;

  /* Optional linkage to the shared contract concepts */
  char** criteria_touched;  /* array of criteria IDs (owned by agenda) */
  size_t criteria_touched_count;

  char** option_refs;       /* array of option IDs (owned by agenda) */
  size_t option_refs_count;
} gh_agenda_item_t;

/* Milestone: a due date + what it’s for. */
typedef struct gh_milestone {
  char* milestone_id;  /* owned */
  char* title;         /* owned */
  char* notes;         /* optional, owned (may be NULL) */

  gh_rfc3339_t due_at; /* string view unless copied */
  char* owner_id;      /* optional participant id, owned (may be NULL) */

  /* status: "open", "in_progress", "done", "dropped" (owned, may be NULL) */
  char* status;
} gh_milestone_t;

/* Session metadata relevant to scheduling. */
typedef struct gh_session_info {
  char* session_id; /* owned */
  char* title;      /* owned */
  gh_vibe_t vibe;
  char* vibe_notes; /* optional, owned (may be NULL) */

  gh_rfc3339_t started_at; /* string view unless copied */
  gh_rfc3339_t ended_at;   /* optional string view; ended_at.s may be NULL */
} gh_session_info_t;

/* --------------------------- Containers --------------------------- */

/* Opaque handle for a calende document/workspace. */
typedef struct gh_calende gh_calende_t;

/*
  Create/destroy the calende workspace.

  - gh_calende_create allocates a new workspace.
  - gh_calende_destroy frees everything associated with it.
*/
gh_calende_t* gh_calende_create(void);
void gh_calende_destroy(gh_calende_t* cal);

/* Clear all data but keep the workspace allocated. */
void gh_calende_clear(gh_calende_t* cal);

/* ------------------------- Session control ------------------------ */

/*
  Set session info. Strings are copied into the workspace.
  Passing NULL for optional fields clears them.
*/
gh_calende_status_t gh_calende_set_session_info(
    gh_calende_t* cal,
    const char* session_id,
    const char* title,
    gh_vibe_t vibe,
    const char* vibe_notes,
    const char* started_at_rfc3339,
    const char* ended_at_rfc3339 /* may be NULL */
);

/* Get a read-only view into stored session info. Pointers remain valid until clear/destroy. */
gh_calende_status_t gh_calende_get_session_info(const gh_calende_t* cal, gh_session_info_t* out_view);

/* ------------------------- Agenda management ---------------------- */

/*
  Add an agenda item. All strings are copied.
  criteria_touched and option_refs arrays are copied (each string copied).
*/
gh_calende_status_t gh_calende_agenda_add_item(
    gh_calende_t* cal,
    const char* item_id,
    const char* title,
    const char* description, /* may be NULL */
    unsigned int timebox_minutes,
    unsigned int order,
    const char* const* criteria_touched,
    size_t criteria_touched_count,
    const char* const* option_refs,
    size_t option_refs_count
);

/* Remove agenda item by ID. */
gh_calende_status_t gh_calende_agenda_remove_item(gh_calende_t* cal, const char* item_id);

/* Count agenda items. */
size_t gh_calende_agenda_count(const gh_calende_t* cal);

/*
  Get a read-only view of an agenda item by index (0..count-1).
  The returned view's pointers remain valid until clear/destroy or the item is removed.
*/
gh_calende_status_t gh_calende_agenda_get_by_index(const gh_calende_t* cal, size_t index, gh_agenda_item_t* out_view);

/* Sort agenda items by (order, then insertion). */
gh_calende_status_t gh_calende_agenda_sort(gh_calende_t* cal);

/* Compute total timebox minutes across all items where timebox_minutes != 0. */
unsigned int gh_calende_agenda_total_timebox_minutes(const gh_calende_t* cal);

/* ------------------------ Milestone management -------------------- */

/* Add a milestone. All strings are copied. */
gh_calende_status_t gh_calende_milestone_add(
    gh_calende_t* cal,
    const char* milestone_id,
    const char* title,
    const char* notes, /* may be NULL */
    const char* due_at_rfc3339, /* may be NULL */
    const char* owner_id,       /* may be NULL */
    const char* status          /* may be NULL */
);

gh_calende_status_t gh_calende_milestone_remove(gh_calende_t* cal, const char* milestone_id);
size_t gh_calende_milestone_count(const gh_calende_t* cal);
gh_calende_status_t gh_calende_milestone_get_by_index(const gh_calende_t* cal, size_t index, gh_milestone_t* out_view);

/* ----------------------------- JSON ------------------------------- */

/*
  JSON I/O integration points.

  The Great Hall shared contract includes:
    - meta/session (we manage session subset)
    - settings/options/criteria_set/discussion_rows/decisions/action_items (handled elsewhere)
  calende focuses on agenda + milestones but can serialize into an extension field.

  Recommended convention (non-breaking):
    - Store calende-specific data under:  "extensions": { "calende": { ... } }

  Implementations may:
    - Parse/emit JSON using a library (recommended).
    - Or use a minimal serializer if strict control is desired.
*/

/*
  Import from JSON text.
  - json_utf8: NUL-terminated UTF-8 JSON string.
  - Accepts either:
      (a) full Great Hall document containing extensions.calende
      (b) a calende-only JSON object (implementation-defined)
*/
gh_calende_status_t gh_calende_import_json(gh_calende_t* cal, const char* json_utf8);

/*
  Export to JSON text.
  - If out_json_utf8 is NULL or out_cap is 0, returns required size via out_required (including NUL).
  - Otherwise writes a NUL-terminated JSON string to out_json_utf8.
*/
gh_calende_status_t gh_calende_export_json(
    const gh_calende_t* cal,
    char* out_json_utf8,
    size_t out_cap,
    size_t* out_required /* may be NULL */
);

/* --------------------------- Utilities ---------------------------- */

/* Validate basic invariants (IDs present, etc.). Does not guarantee schema-level validity. */
gh_calende_status_t gh_calende_validate(const gh_calende_t* cal);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* GREAT_HALL_CALENDE_H */