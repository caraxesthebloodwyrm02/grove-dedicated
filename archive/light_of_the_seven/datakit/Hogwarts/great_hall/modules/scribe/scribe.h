#ifndef GREAT_HALL_SCRIBE_H
#define GREAT_HALL_SCRIBE_H

/*
  scribe.h — Great Hall "scribe" module (C)

  Purpose:
    - Capture conversation into structured "discussion rows"
    - Maintain a decision log and action items
    - Import/export JSON compatible with the Great Hall shared contract

  Intended contract alignment:
    - OPEN_POLICY.md defines the shared JSON contract keys:
        meta, session, criteria_set, settings, options,
        discussion_rows, decisions, action_items, calculator_results (optional)
    - scribe focuses on:
        discussion_rows, decisions, action_items
      and may optionally embed under:
        extensions.scribe
      if used standalone.

  Notes:
    - This is a header-only skeleton; implement in scribe.c.
    - JSON is handled as UTF-8 text. Use a JSON library in the implementation.
    - Ownership rules:
        * API input strings are copied into the scribe workspace unless explicitly stated.
        * Getters return views; pointers remain valid until overwritten, cleared, or destroyed.
*/

#include <stddef.h> /* size_t */

#ifdef __cplusplus
extern "C" {
#endif

/* ---------------------------- Versioning ---------------------------- */

#define GH_SCRIBE_VERSION_MAJOR 1
#define GH_SCRIBE_VERSION_MINOR 0
#define GH_SCRIBE_VERSION_PATCH 0

/* ----------------------------- Status ------------------------------ */

typedef enum gh_scribe_status {
  GH_SCRIBE_OK = 0,
  GH_SCRIBE_ERR_INVALID_ARGUMENT = 1,
  GH_SCRIBE_ERR_OUT_OF_MEMORY = 2,
  GH_SCRIBE_ERR_PARSE = 3,
  GH_SCRIBE_ERR_NOT_FOUND = 4,
  GH_SCRIBE_ERR_BUFFER_TOO_SMALL = 5,
  GH_SCRIBE_ERR_IO = 6,
  GH_SCRIBE_ERR_INTERNAL = 100
} gh_scribe_status_t;

/* Convert a status code to a stable string literal (never NULL). */
const char* gh_scribe_status_str(gh_scribe_status_t status);

/* ------------------------------ Time ------------------------------- */

/* RFC3339 timestamp string view. */
typedef struct gh_rfc3339 {
  const char* s; /* Not owned unless copied into module storage. */
} gh_rfc3339_t;

/* -------------------------- Enumerations --------------------------- */

/*
  discussion_rows.kind values aligned with OPEN_POLICY.md:
    question, claim, evidence, proposal, bridge, decision, note
*/
typedef enum gh_row_kind {
  GH_ROW_QUESTION = 0,
  GH_ROW_CLAIM = 1,
  GH_ROW_EVIDENCE = 2,
  GH_ROW_PROPOSAL = 3,
  GH_ROW_BRIDGE = 4,
  GH_ROW_DECISION = 5,
  GH_ROW_NOTE = 6
} gh_row_kind_t;

typedef enum gh_decision_status {
  GH_DECISION_MADE = 0,
  GH_DECISION_DEFERRED = 1,
  GH_DECISION_REVERSED = 2
} gh_decision_status_t;

typedef enum gh_action_status {
  GH_ACTION_OPEN = 0,
  GH_ACTION_IN_PROGRESS = 1,
  GH_ACTION_DONE = 2,
  GH_ACTION_DROPPED = 3
} gh_action_status_t;

/* ------------------------ Core record types ------------------------ */

typedef struct gh_discussion_row {
  char* row_id;         /* owned (stable ID) */
  gh_rfc3339_t at;      /* string view unless copied */
  char* speaker_id;     /* owned (participant id) */
  gh_row_kind_t kind;

  /* Human-readable narrative text. */
  char* content;        /* owned */

  /* Optional linkage for table comprehension */
  char** criteria_touched; /* owned array of owned strings; may be NULL */
  size_t criteria_touched_count;

  char** option_refs;      /* owned array of owned strings; may be NULL */
  size_t option_refs_count;

  /* Optional backreferences (IDs) */
  char* decision_ref;   /* owned; may be NULL */
  char* action_ref;     /* owned; may be NULL */

  /* Optional context tag; not for policing. */
  char* tone_tag;       /* owned; may be NULL */
} gh_discussion_row_t;

typedef struct gh_decision {
  char* decision_id;         /* owned */
  gh_rfc3339_t at;           /* string view unless copied */
  char* title;               /* owned */
  gh_decision_status_t status;

  char* summary;             /* optional, owned (may be NULL) */
  char* chosen_option_id;    /* optional, owned (may be NULL) */
  char* rationale;           /* optional, owned (may be NULL) */

  /*
    "Meet halfway" bridge:
      - minimum viable compromise
      - time-boxed trial
      - fallback plan
      - testable condition to change mind
  */
  char* bridge_used;         /* optional, owned (may be NULL) */
} gh_decision_t;

typedef struct gh_action_item {
  char* action_id;       /* owned */
  char* title;           /* owned */
  char* owner_id;        /* owned (participant id) */
  gh_rfc3339_t due_at;   /* optional; due_at.s may be NULL */
  gh_action_status_t status;
  char* notes;           /* optional, owned (may be NULL) */
} gh_action_item_t;

/* -------------------------- Opaque handles ------------------------- */

typedef struct gh_scribe gh_scribe_t;

/* ---------------------- Workspace lifecycle ------------------------ */

gh_scribe_t* gh_scribe_create(void);
void gh_scribe_destroy(gh_scribe_t* s);
void gh_scribe_clear(gh_scribe_t* s);

/* ------------------------- Row management -------------------------- */

/*
  Add a discussion row.
  - All strings are copied into the workspace.
  - Arrays criteria_touched and option_refs are copied (each element copied).
  - at_rfc3339 may be NULL; implementations may insert a timestamp if configured.
*/
gh_scribe_status_t gh_scribe_add_row(
    gh_scribe_t* s,
    const char* row_id,
    const char* at_rfc3339,     /* may be NULL */
    const char* speaker_id,
    gh_row_kind_t kind,
    const char* content,
    const char* const* criteria_touched,
    size_t criteria_touched_count,
    const char* const* option_refs,
    size_t option_refs_count,
    const char* decision_ref,   /* may be NULL */
    const char* action_ref,     /* may be NULL */
    const char* tone_tag        /* may be NULL */
);

/* Remove a row by ID. */
gh_scribe_status_t gh_scribe_remove_row(gh_scribe_t* s, const char* row_id);

size_t gh_scribe_row_count(const gh_scribe_t* s);

/*
  Get row by index (0..count-1).
  - out_view receives pointers into internal storage (do not free).
  - Valid until clear/destroy or the row is removed/overwritten.
*/
gh_scribe_status_t gh_scribe_get_row_by_index(
    const gh_scribe_t* s,
    size_t index,
    gh_discussion_row_t* out_view
);

/*
  Find row by ID (linear search unless implementation uses a map).
  Returns GH_SCRIBE_ERR_NOT_FOUND if missing.
*/
gh_scribe_status_t gh_scribe_get_row_by_id(
    const gh_scribe_t* s,
    const char* row_id,
    gh_discussion_row_t* out_view
);

/* ------------------------ Decision management ---------------------- */

/*
  Add a decision. Strings are copied.
  - at_rfc3339 may be NULL.
*/
gh_scribe_status_t gh_scribe_add_decision(
    gh_scribe_t* s,
    const char* decision_id,
    const char* at_rfc3339,        /* may be NULL */
    const char* title,
    gh_decision_status_t status,
    const char* summary,           /* may be NULL */
    const char* chosen_option_id,  /* may be NULL */
    const char* rationale,         /* may be NULL */
    const char* bridge_used        /* may be NULL */
);

gh_scribe_status_t gh_scribe_remove_decision(gh_scribe_t* s, const char* decision_id);

size_t gh_scribe_decision_count(const gh_scribe_t* s);

gh_scribe_status_t gh_scribe_get_decision_by_index(
    const gh_scribe_t* s,
    size_t index,
    gh_decision_t* out_view
);

gh_scribe_status_t gh_scribe_get_decision_by_id(
    const gh_scribe_t* s,
    const char* decision_id,
    gh_decision_t* out_view
);

/* ----------------------- Action item management --------------------- */

/*
  Add an action item. Strings are copied.
  - due_at_rfc3339 may be NULL (no due date).
*/
gh_scribe_status_t gh_scribe_add_action_item(
    gh_scribe_t* s,
    const char* action_id,
    const char* title,
    const char* owner_id,
    const char* due_at_rfc3339, /* may be NULL */
    gh_action_status_t status,
    const char* notes           /* may be NULL */
);

gh_scribe_status_t gh_scribe_remove_action_item(gh_scribe_t* s, const char* action_id);

size_t gh_scribe_action_item_count(const gh_scribe_t* s);

gh_scribe_status_t gh_scribe_get_action_item_by_index(
    const gh_scribe_t* s,
    size_t index,
    gh_action_item_t* out_view
);

gh_scribe_status_t gh_scribe_get_action_item_by_id(
    const gh_scribe_t* s,
    const char* action_id,
    gh_action_item_t* out_view
);

/* ------------------------ Convenience helpers ---------------------- */

/*
  Link a discussion row to an existing decision/action by setting refs.
  - If the row does not exist -> NOT_FOUND.
  - If decision_id/action_id provided but not present, implementation may:
      * allow dangling refs (more flexible), or
      * return NOT_FOUND (stricter)
    Choose behavior in scribe.c; document it there.
*/
gh_scribe_status_t gh_scribe_row_set_refs(
    gh_scribe_t* s,
    const char* row_id,
    const char* decision_id, /* may be NULL to clear */
    const char* action_id    /* may be NULL to clear */
);

/*
  Meet-halfway enforcement (optional):
  Validate that for decisions with status==MADE, bridge_used is present.
  If enforce_bridge == 1 and a made decision lacks a bridge, return INVALID_ARGUMENT.
*/
gh_scribe_status_t gh_scribe_validate_policy(
    const gh_scribe_t* s,
    int enforce_bridge
);

/* ------------------------------ JSON -------------------------------- */

/*
  Import from JSON text (UTF-8, NUL-terminated).
  Accepts either:
    (a) full Great Hall document containing discussion_rows/decisions/action_items
    (b) scribe-only object (implementation-defined)
*/
gh_scribe_status_t gh_scribe_import_json(gh_scribe_t* s, const char* json_utf8);

/*
  Export to JSON text.
  If out_json_utf8 is NULL or out_cap == 0, returns required size via out_required (including NUL).
  Otherwise writes a NUL-terminated JSON string.
*/
gh_scribe_status_t gh_scribe_export_json(
    const gh_scribe_t* s,
    char* out_json_utf8,
    size_t out_cap,
    size_t* out_required /* may be NULL */
);

/* ----------------------------- Validation --------------------------- */

/*
  Basic internal validation (IDs present, etc.). Not full JSON-schema validation.
*/
gh_scribe_status_t gh_scribe_validate(const gh_scribe_t* s);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* GREAT_HALL_SCRIBE_H */