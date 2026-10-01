# STANDARDS-FORMAT
# build-standards

What belongs in a standards file, and the form its rules and audit instructions take. Load it when writing or auditing a file in the standards family — never at session startup.

The family is `common-standards.md` plus one file per governed artifact class. Those files state rules about artifacts; this one states their shared form.

---

## The family's structural contract

`common-standards.md` holds every rule that is the same for all four governed classes. Under any such rule it also states how that rule resolves for a named class, in a `Class deltas` block inside that rule's section. A delta stated there is not a rule of its own and has no meaning apart from the rule above it; a per-class statement standing free of such a rule has no home in the core. A `Class deltas` block either carries the delta's content or names the class file that owns it, and a delta whose content is a body of rules a class file holds in full is stated by naming that file. A class file states only what differs for its class, and never restates a rule from the core or from another class file. A class file closes on a pointer to the core naming its own deltas.

Every rule in the family has exactly one owner. A pointer sentence naming another file as the owner is not a second statement of the rule; a sentence carrying the rule's content is, however it is framed — as an example, a summary, a reminder or a convenience copy. A rule that cannot be assigned to one owner is evidence that a boundary sits in the wrong place.

A pointer resolves: the file it names states the rule it names. A pointer whose target does not state the rule leaves that rule owned by nobody, and two files each naming the other as owner leave it stated nowhere while reading as owned from either side. A pointer may name a file, or name a class whose standard is meant; both are pointers and both resolve.

Two files stating the same content hold one rule only where that content derives from a single constraint reaching both, such that a change to it for one holder makes the other wrong. Where each statement rests on its own holder's properties, and either could change while the other stays correct, they are two rules that coincide, each owned where it sits, and the agreement between them is not a second statement of one rule.

A rule deriving from a single constraint and holding for some classes and not all has no home in the core and no home in a class file that states it as though it were a class delta. It sits with the class that states it most fully, and every other file needing it points there by name.

**Audit checkpoint:** For every rule the file states, search the other files in the family for the same rule; for each match, name the single constraint both statements derive from, and report the rule as stated in more than one file, with both locations and both wordings. Where no such constraint can be named and each statement rests on its own holder's properties, the two coincide and neither is a finding. Where the file is the core, confirm every rule it states holds for all four classes, and that every per-class statement sits in a `Class deltas` block under such a rule. Flag a per-class statement standing free of one, a `Class deltas` block that neither carries the delta's content nor names the class file owning it, and a `Class deltas` block carrying in full a body of rules that a class file holds. Where it is a class file, confirm it states its class's genuine differences and nothing holding for every class, and that it closes on a pointer naming its deltas rather than restating them. For a rule deriving from a single constraint and holding for some classes and not all, confirm exactly one file states it and every other names that file. For every sentence naming another file, or naming a class whose standard is meant, as a rule's owner, read that file at the named rule and confirm it states it; flag a pointer whose target does not, and every pair of files each naming the other as owner of the same rule.

**Judgment call:** whether one constraint reaches both statements, or each rests on its own holder's properties, is read from the meaning of the two passages rather than from any property of either file. It is confirmed with the contributor where the reading is not obvious.

---

## Rule form

The property form every rule takes, and the four shapes that fail it, hold for every governed artifact and are stated in `common-standards.md` under Rule form. Every file in this family is governed by it.

---

## Audit checkpoints

Every rule states a property an audit can confirm against a file, or is marked a judgment call. There is no third category.

`Audit checkpoint:` closes every section that states a rule, and carries the instruction for checking it. The instruction names an observable property of a file; one asking the reader to judge intent, or naming no property at all, checks nothing. The requirement is per rule rather than per section: every rule a section states is reached by its checkpoint. A definitional section, a pointer section and a shared-rules section state no rule of their own and carry no checkpoint.

`Judgment call:` marks a rule, or the part of a checkpoint, resting on something a file does not hold — a contributor population, session history, or the meaning a reader takes from a name or a passage. The marking names what cannot be read from the file, and who confirms it. A rule of this kind carrying no marking reads as checkable while nothing can check it.

**Audit checkpoint:** For every section, state whether it holds a rule. Where it does, confirm an `Audit checkpoint:` line closes it and that every rule the section states is reached by that line. Flag a rule no checkpoint reaches, a checkpoint instruction naming no observable property of a file, a rule or a part of a checkpoint resting on anything outside the file that carries no `Judgment call:` marking, and a `Judgment call:` marking that does not name both what cannot be read from the file and who confirms it.

---

## Claims about the text

No checkpoint instruction directs the reader at a status marker, certification claim, approval note, byte count or worklog entry in place of the content it describes. Each is a claim about the text and not the text.

**Audit checkpoint:** Flag every checkpoint instruction in the file that directs the reader at a status marker, a certification claim, an approval note, a byte count or a worklog entry in place of the content it describes.

---

## Rules stated elsewhere

Instruction cleanliness and the external-reference class line hold for every governed artifact and are stated in `common-standards.md`. Every file in this family is governed by both, as it is by Rule form above.
