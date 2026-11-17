---
layout: archive
title: "Group"
permalink: /group/
author_profile: true
---
<link rel="stylesheet" href="{{ '/assets/css/group.css' | relative_url }}">

<div class="group-page">
  <p class="group-intro">The <strong>Gravitational-Wave Astrophysics Group</strong> is led by <a href="{{ '/' | relative_url }}">Prof. Yan Wang</a> at the <a href="https://ngl.hust.edu.cn">National Gravitational Laboratory</a> and <a href="http://phys.hust.edu.cn">School of Physics</a>, <a href="https://www.hust.edu.cn">Huazhong University of Science and Technology</a> (HUST).</p>

  <nav class="group-index" aria-label="Group sections">
    <a href="#current-students">Current students</a>
    <a href="#graduate-alumni">Graduate alumni</a>
    <a href="#former-postdocs">Former postdoctoral researchers</a>
    <a href="#former-members">Former members</a>
  </nav>

  <section aria-labelledby="current-students">
    <h2 id="current-students">Current Graduate Students</h2>
    <h3 class="group-subheading">PhD Students <span class="group-count">({{ site.data.group_members.phd_students.size }})</span></h3>
    <ul class="group-members" data-member-group="phd_students">
      {% for member in site.data.group_members.phd_students %}
        {% include group-member.html member=member heading="h4" %}
      {% endfor %}
    </ul>

    <h3 class="group-subheading">Master's Students <span class="group-count">({{ site.data.group_members.masters_students.size }})</span></h3>
    <ul class="group-members" data-member-group="masters_students">
      {% for member in site.data.group_members.masters_students %}
        {% include group-member.html member=member heading="h4" %}
      {% endfor %}
    </ul>
  </section>

  <section aria-labelledby="graduate-alumni">
    <h2 id="graduate-alumni">Graduate Alumni</h2>
    <ul class="group-members" data-member-group="graduate_alumni">
      {% for member in site.data.group_members.graduate_alumni %}
        {% include group-member.html member=member %}
      {% endfor %}
    </ul>
  </section>

  <section aria-labelledby="former-postdocs">
    <h2 id="former-postdocs">Former Postdoctoral Researchers</h2>
    <ul class="group-members" data-member-group="former_postdocs">
      {% for member in site.data.group_members.former_postdocs %}
        {% include group-member.html member=member %}
      {% endfor %}
    </ul>
  </section>

  <section aria-labelledby="former-members">
    <h2 id="former-members">Former Members</h2>
    <ul class="group-members" data-member-group="former_members">
      {% for member in site.data.group_members.former_members %}
        {% include group-member.html member=member %}
      {% endfor %}
    </ul>
  </section>
</div>
